from datetime import datetime, timedelta
import requests
from extensions.extensions import application_config, logger, db, refresh_token_url, auth_url
from models.authtoken_model import AuthToken
 

department_id = application_config["department_id"]
token_life_margin = application_config["lims"]["authentication"]["refresh_threshold"]

def _get_jwt_token() -> dict | None:
    params = {
        "username": application_config["lims"]["authentication"]["username"],
        "password": application_config["lims"]["authentication"]["password"]
    }
    try:
       
        response = requests.post(auth_url, data=params)
        response.raise_for_status()
        if response.status_code == 200:
            response_json = response.json()
            return {
                "token": response_json.get("authorization").get("token"),
                "expires_at": response_json.get("authorization").get("expiry_time")
            }
        else:
            raise ValueError("Unexpected response from authentication service")
    except requests.RequestException as e:
        logger.error(f"Error fetching JWT token: {e}")
        return None
    except Exception as e:
        logger.error("error: %s", e)
        return None

def _summon_token()-> dict | None: # create a new token
    new_token = _get_jwt_token()
    logger.info(f"Token: {new_token}")
    try:
        department_auth = db.session.query(AuthToken).filter(
            AuthToken.department_id == department_id
        ).first() # Add parentheses to .first()
        if (department_auth):
            db.session.query(AuthToken).filter(
                AuthToken.department_id == department_id
            ).update(
                {
                    AuthToken.auth_token: new_token.get("token"),
                    AuthToken.expires_at: datetime.fromisoformat(
                        new_token.get("expires_at").replace("Z", "+00:00")).replace(tzinfo=None),
                    AuthToken.issued_at: datetime.now()
                }
            )
        else:
            db.session.add(AuthToken(
                auth_token=new_token.get("token"),
                expires_at=datetime.fromisoformat(
                    new_token.get("expires_at").replace("Z", "+00:00")).replace(tzinfo=None),
                issued_at=datetime.utcnow(),
                department_id=department_id
            ))
        db.session.commit()

        return new_token
    except Exception as e:
        logger.error("error: %s", e)

def _revive_token() -> dict | None:
    
    local_token = db.session.query(AuthToken).filter(
        AuthToken.department_id == department_id
    ).first()
    if not local_token:
        logger.info("Returned none on tokken revive")
        return None
    try:
        response = requests.get(refresh_token_url, headers={"Authorization": f"Bearer {local_token.auth_token}"})
        if response.status_code != 200:
            logger.warning(f"token was invalidated")
            _summon_token()
        response.raise_for_status()
        token_reborn = response.json()
        existing_token = db.session.query(AuthToken).filter(
            AuthToken.department_id == department_id
        ).update(
            {
                AuthToken.auth_token: token_reborn.get("authorization").get("token"),
                AuthToken.expires_at: datetime.fromisoformat(
                    token_reborn.get("authorization").get("expiry_time").replace("Z", "+00:00")).replace(tzinfo=None),
                AuthToken.issued_at: datetime.utcnow()
            }
        )
        if not existing_token:
            logger.error("Failed to update the token in the database.")
            return None
        else:
            logger.info("Token successfully updated in the database.")
            db.session.commit()
        return token_reborn
    except requests.RequestException as e:
        logger.error("error: %s", e)
        return None
    except Exception as e:
        logger.error("error: %s", e)
        return None
    


def validate_token_life() -> bool:
    local_token = db.session.query(AuthToken).filter(
        AuthToken.department_id == department_id
    ).first()
    
    # No token exists, summon a new one
    if not local_token:
        logger.info("No local token found, summoning a new one.")
        return _summon_token() is not None

    now = datetime.utcnow()

    # Token expired
    if local_token.expires_at <= now:
        logger.warning("Token has expired, summoning a new one.")
        return _summon_token() is not None

    # Token is about to expire (within threshold)
    if local_token.expires_at - now < timedelta(minutes=token_life_margin):
        logger.info("Token is nearing expiry, reviving token.")
        _revive_token() is not None
        return True

        

    # Token is valid and not near expiry
    return True


def release_the_token() -> str | None:
    local_token = db.session.query(AuthToken).filter(
            AuthToken.department_id == department_id
        ).first()
    if local_token:
        return local_token.auth_token
    return None