import datetime
import requests
from extensions.extensions import application_config, logger, db
from models.authtoken_model import AuthToken
 

department_id = application_config["department_id"]
token_life_margin = application_config["lims"]["authentication"]["refresh_threshhold"]

def _get_jwt_token() -> dict | None:
    auth_url = application_config["lims"]["base_url"] + application_config["lims"]["authentication"]["auth_endpoint"]
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
                "token": response_json.get("token"),
                "expires_at": response_json.get("expiry_time")
            }
        else:
            raise ValueError("Unexpected response from authentication service")
    except requests.RequestException as e:
        logger.error(f"Error fetching JWT token: {e}")
        return None
    except Exception as e:
        logger.error("error: %s", e)
        return None

def _summon_token()-> dict | None:
    new_token = _get_jwt_token()
    try:
        db.session.query(AuthToken).filter(
            AuthToken.department_id == department_id
        ).update(
            {
                AuthToken.auth_token: new_token.get("token"),
                AuthToken.expires_at: new_token.get("expires_at"),
                AuthToken.issued_at: datetime.utcnow()
            }
        )
        db.session.commit()

        return new_token
    except Exception as e:
        logger.error("error: %s", e)

def _revive_token() -> dict | None:
    api_key = application_config["lims"]["authentication"]["refresh_token_endpoint"]
    refresh_token_url = application_config["lims"]["base_url"] + api_key
    local_token = db.session.query(AuthToken).filter(
        AuthToken.department_id == department_id
    ).first()
    if not local_token:
        return None
    try:
        response = requests.get(refresh_token_url, headers={"Authorization": f"Bearer {local_token.auth_token}"})
        response.raise_for_status()
        token_reborn = response.json()
        db.session.query(AuthToken).filter(
            AuthToken.department_id == department_id
        ).update(
            {
                AuthToken.auth_token: token_reborn.get("token"),
                AuthToken.expires_at: token_reborn.get("expiry_time"),
                AuthToken.issued_at: datetime.utcnow()
            }
        )
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
    if local_token.expires_at - now < datetime.timedelta(minutes=token_life_margin):
        logger.info("Token is nearing expiry, reviving token.")
        return _revive_token() is not None

    # Token is valid and not near expiry
    return True


def release_token() -> str | None:
    local_token = db.session.query(AuthToken).filter(
            AuthToken.department_id == department_id
        ).first()
    if local_token:
        return local_token.auth_token
    return None