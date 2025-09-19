import requests
from extensions.extensions import logger, TEST_LIST_URL, FETCH_START_DATE,\
    FETCH_END_DATE, DEPARTMENT_ID, LAB_LOCATION_ID, MINIMAL
from services.auth_service import validate_token_life, release_the_token


def fetch_test_batch():
    params = {
        "lab_location": LAB_LOCATION_ID,
        "department_id": DEPARTMENT_ID, 
        "minimal": MINIMAL,
        "start_date": FETCH_START_DATE,
        "end_date": FETCH_END_DATE
    }

    
    if not validate_token_life():
        logger.warning("Token validation failed.")
        return None

    headers = {"Authorization": f"Bearer {release_the_token()}"}
    response = requests.get(TEST_LIST_URL, headers=headers, data=params)
    if response.status_code == 200:
        logger.info(f"successfully fetched test data: {params.get('start_date')}")
        return response.json()
    return None
