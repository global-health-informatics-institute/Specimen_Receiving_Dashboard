
from flask import Blueprint, json, request, jsonify
from apis.misc import map_lims_to_oerr_dashboard_status
from apis.weekly_count_api import weekly_increment as weekly_increment_api
from apis.monthly_count_api import monthly_increment as monthly_increment_api
from extensions.extensions import logger, db
from sqlalchemy.exc import SQLAlchemyError
from models.tests_model import Test

load_entries_bp = Blueprint('load_entries', __name__)

STATUS_VOIDED = 0
STATUS_NEW = 1


# extract required fields from the payload
def process_payload(payload):
    def actual_status(specimen_status, test_status):
        return map_lims_to_oerr_dashboard_status(test_status, specimen_status)
    
    def get_status_info():
        return actual_status(payload.get("order_status"), payload.get("status"))
    
    def get_test_type():
        return  payload.get("test_type_id")
    
    def get_accession_number():
        return  payload.get("accession_number")
    
    def get_department_id():
        return payload.get("specimen_id")
    
    test_status = get_status_info()
    test_type = get_test_type()
    accession_number = get_accession_number()
    department_id = get_department_id()
    return accession_number, test_status, test_type, department_id


@load_entries_bp.route('/save_entry/', methods=['POST'])
def save_entry():
    try:
        # Step 1: Validate the request data
        if not request.is_json:
            logger.error("Invalid request, JSON data is required")
            return jsonify({"message": "Invalid request, JSON data is required"}), 415
                
        data = request.get_json()

        if not data:
            return jsonify({"message": "Invalid request, JSON data is required"}), 400
        
        if data is None:
            logger.error("No JSON data provided or JSON is malformed")
            return jsonify({"message": "Invalid or missing JSON data"}), 400


        # Step 2: Extract required fields
        accession_number,test_status,test_type, department_id = process_payload(data)

        if not accession_number:
            logger.error("Missing required field: accession_number")
            return jsonify({"message": "Missing required field: accession_number"}), 400
        
        if test_status is None:
            logger.error("Missing required field: test_status")
            return jsonify({"message": "Missing required field: test_status"}), 400
        
        if not test_type:
            logger.error("Missing required field: test_type")
            return jsonify({"message": "Missing required field: test_type"}), 400
        
        if not department_id:
            logger.error("Missing required field: department_id")
            return jsonify({"message": "Missing required field: department_id"}), 400

        
        # query the database to check if the test already exists
        existing_test = db.session.query(Test).filter_by(
            test_accession_id=accession_number,
            test_test_type=test_type
        ).first()


        # TODO: check with egpaf, how multiple tests are tied to a single accession number
            # consider checking through an array, or continue handling it as a single json
        unchanged_test = db.session.query(Test).filter_by(
            test_test_status=test_status,
            test_accession_id=accession_number,
            test_test_type=test_type
        ).first()
        
        if existing_test:
            logger.info(f"Existing test found: {accession_number}, {test_type}, {test_status}")
            if int(existing_test.test_test_status) in [0,9]:
                logger.warning(f"Test is voided or cancelled, no updates allowed: {accession_number}, {test_type}, {test_status}")
                logger.info(f"Test state: {existing_test.test_test_status}")
                return jsonify({"message": "Test is voided or cancelled, no updates allowed"}), 403

            if unchanged_test:
                logger.warning(f"Test already exists: {accession_number}, {test_type}, {test_status}")
                return jsonify({"message": "Test with this accession number and same test type already exists with the same status"}), 304
            else:
                logger.error("Existing test found, updating status")

                # check if the current status, and the update status are next to each other(have a difference of 1, i.e no status was skipped)
                if int(existing_test.test_test_status) +1 == int(test_status) or int(test_status) == 0:
                    db.session.query(Test).filter_by(test_accession_id=accession_number).update({"test_test_status": str(test_status)})
                    weekly_increment_api(department_id, test_status)
                    monthly_increment_api(department_id, test_status)
                    logger.info(f"updated existing test {accession_number}")
                else:
                    diff = test_status - int(existing_test.test_test_status) 
                    while diff > 0:
                        weekly_increment_api(department_id, test_status - (diff-1))
                        monthly_increment_api(department_id, test_status - (diff-1))
                        diff-=1
                    db.session.query(Test).filter_by(test_accession_id=accession_number).update({"test_test_status": test_status})
                    logger.info(f"updated existing test- Multiply counts {accession_number}")

                    
        else: #its a new test
            logger.info(f"Creating new test: {accession_number}, {test_type}, {test_status}, {department_id}")
            new_test = Test(
                test_test_status = test_status,
                test_accession_id = accession_number,
                test_test_type = test_type
            )
            if test_status == 1:
                db.session.add(new_test)
                weekly_increment_api(department_id, test_status)
                monthly_increment_api(department_id, test_status)
                logger.info(f"added new test - New {accession_number}")

            
            if test_status == STATUS_VOIDED:
                db.session.add(new_test)
                weekly_increment_api(department_id, test_status)
                monthly_increment_api(department_id, test_status)
                weekly_increment_api(department_id, 1)
                monthly_increment_api(department_id, 1)
                logger.info(f"added new test - voided {accession_number}")

            
            if test_status != STATUS_NEW and test_status !=STATUS_VOIDED:
                db.session.add(new_test)
                i =  test_status
                while i > 0:
                    weekly_increment_api(department_id, i)
                    monthly_increment_api(department_id, i)
                    i-=1
                logger.info(f"added new test - Multiply counts {accession_number}")
        

            


        db.session.commit()
        return jsonify({"message": "Entry saved successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error: {str(e)}")
        return jsonify({"message": "An error occurred while saving the entry"}), 500
    
    except TypeError as e:
        db.session.rollback()
        logger.error(f"Type error: {str(e)}")
        return jsonify({"message": "Invalid data type provided"}), 415

    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "An unexpected error occurred"}), 500


"""
Example of request
'
{
    "id": 25,
    "order_id": 15,
    "specimen_id": 3,
    "specimen_type": "Blood",
    "test_panel_id": None,
    "test_panel_name": None,
    "created_date": "2024-12-06T06:42:09.310Z",
    "request_origin": "In Patient",
    "requesting_ward": "MSS",
    "accession_number": "KCH2400000012",
    "test_type_id": 35,
    "test_type_name": "FBC",
    "tracking_number": "XKCH2400000012",
    "voided": 0,
    "requested_by": "maganga",
    "completed_by": {},
    "client": {
        "id": 7,
        "first_name": "Test",
        "middle_name": "",
        "last_name": "Patient",
        "sex": "F",
        "date_of_birth": "1992-07-05",
        "birth_date_estimated": 0,
        "client_history": "identical 2"
    },
    "status": "pending",
    "order_status": "specimen-not-collected",
    "lab_location": {
        "id": 1,
        "name": "Main Lab"
    },
    "is_machine_oriented": True,
    "result_remarks": None,
    "indicators": [
        {
            "id": 169,
            "name": "WBC",
            "test_indicator_type": "numeric",
            "unit": "10^3/uL",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 764,
                    "test_indicator_id": 169,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "4.0",
                    "upper_range": "10.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 147,
            "name": "RBC",
            "test_indicator_type": "numeric",
            "unit": "10^6/uL",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 710,
                    "test_indicator_id": 147,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "4.0",
                    "upper_range": "6.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 148,
            "name": "HGB",
            "test_indicator_type": "numeric",
            "unit": "g/dL",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 714,
                    "test_indicator_id": 148,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "10.9",
                    "upper_range": "17.3",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 149,
            "name": "HCT",
            "test_indicator_type": "numeric",
            "unit": "%",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 718,
                    "test_indicator_id": 149,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "32.0",
                    "upper_range": "50.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 150,
            "name": "MCV",
            "test_indicator_type": "numeric",
            "unit": "fL",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 722,
                    "test_indicator_id": 150,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "71.0",
                    "upper_range": "95.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 151,
            "name": "MCH",
            "test_indicator_type": "numeric",
            "unit": "pg",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 726,
                    "test_indicator_id": 151,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "23.0",
                    "upper_range": "34.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 152,
            "name": "MCHC",
            "test_indicator_type": "numeric",
            "unit": "g/dL",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 728,
                    "test_indicator_id": 152,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "33.0",
                    "upper_range": "36.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 153,
            "name": "PLT",
            "test_indicator_type": "numeric",
            "unit": "10^3/uL",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 730,
                    "test_indicator_id": 153,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "122.0",
                    "upper_range": "330.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 154,
            "name": "RDW-SD",
            "test_indicator_type": "numeric",
            "unit": "fL",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 732,
                    "test_indicator_id": 154,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "37.0",
                    "upper_range": "54.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 155,
            "name": "RDW-CV",
            "test_indicator_type": "numeric",
            "unit": "%",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 734,
                    "test_indicator_id": 155,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "10.0",
                    "upper_range": "16.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 156,
            "name": "PDW",
            "test_indicator_type": "numeric",
            "unit": "fL",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 736,
                    "test_indicator_id": 156,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "9.0",
                    "upper_range": "17.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 157,
            "name": "MPV",
            "test_indicator_type": "numeric",
            "unit": "fL",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 738,
                    "test_indicator_id": 157,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "6.0",
                    "upper_range": "10.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 158,
            "name": "PCT",
            "test_indicator_type": "numeric",
            "unit": "%",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 740,
                    "test_indicator_id": 158,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "0.17",
                    "upper_range": "0.35",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 159,
            "name": "NEUT%",
            "test_indicator_type": "numeric",
            "unit": "%",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 742,
                    "test_indicator_id": 159,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "27.0",
                    "upper_range": "60.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 160,
            "name": "LYMPH%",
            "test_indicator_type": "numeric",
            "unit": "%",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 744,
                    "test_indicator_id": 160,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "29.0",
                    "upper_range": "59.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 161,
            "name": "MONO%",
            "test_indicator_type": "numeric",
            "unit": "%",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 748,
                    "test_indicator_id": 161,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "2.0",
                    "upper_range": "10.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 162,
            "name": "EO%",
            "test_indicator_type": "numeric",
            "unit": "%",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 750,
                    "test_indicator_id": 162,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "0.0",
                    "upper_range": "12.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 163,
            "name": "BASO%",
            "test_indicator_type": "numeric",
            "unit": "%",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 752,
                    "test_indicator_id": 163,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "0.0",
                    "upper_range": "1.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 164,
            "name": "NEUT#",
            "test_indicator_type": "numeric",
            "unit": "10^3/uL",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 754,
                    "test_indicator_id": 164,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "0.82",
                    "upper_range": "4.1",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 165,
            "name": "LYMPH#",
            "test_indicator_type": "numeric",
            "unit": "10^3/uL",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 756,
                    "test_indicator_id": 165,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "1.26",
                    "upper_range": "3.62",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 166,
            "name": "MONO#",
            "test_indicator_type": "numeric",
            "unit": "10^3/uL",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 758,
                    "test_indicator_id": 166,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "0.12",
                    "upper_range": "0.56",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 167,
            "name": "EO#",
            "test_indicator_type": "numeric",
            "unit": "10^3/uL",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 760,
                    "test_indicator_id": 167,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "0.0",
                    "upper_range": "0.78",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 168,
            "name": "BASO#",
            "test_indicator_type": "numeric",
            "unit": "10^3/uL",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 762,
                    "test_indicator_id": 168,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "0.0",
                    "upper_range": "0.07",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 175,
            "name": "P-LCC",
            "test_indicator_type": "numeric",
            "unit": "10^9/L",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 770,
                    "test_indicator_id": 175,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "30.0",
                    "upper_range": "90.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 431,
            "name": "NRBC#",
            "test_indicator_type": "numeric",
            "unit": "10^3/uL",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 1076,
                    "test_indicator_id": 431,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "0.21",
                    "upper_range": "0.63",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 430,
            "name": "NRBC%",
            "test_indicator_type": "numeric",
            "unit": "%",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 1074,
                    "test_indicator_id": 430,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "3.0",
                    "upper_range": "9.2",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 429,
            "name": "RET#",
            "test_indicator_type": "numeric",
            "unit": "10^6/uL",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 1072,
                    "test_indicator_id": 429,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "0.07",
                    "upper_range": "0.131",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 176,
            "name": "P-LCR",
            "test_indicator_type": "numeric",
            "unit": "%",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 772,
                    "test_indicator_id": 176,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "11.0",
                    "upper_range": "45.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 428,
            "name": "RET %",
            "test_indicator_type": "numeric",
            "unit": "%",
            "description": "",
            "result": {},
            "indicator_ranges": [
                {
                    "id": 1070,
                    "test_indicator_id": 428,
                    "sex": "Both",
                    "min_age": 0,
                    "max_age": 120,
                    "lower_range": "0.4",
                    "upper_range": "3.0",
                    "interpretation": "Normal",
                    "value": None
                }
            ]
        },
        {
            "id": 457,
            "name": "Lab Tech. Name:",
            "test_indicator_type": "free_text",
            "unit": "",
            "description": "",
            "result": {},
            "indicator_ranges": []
        }
    ],
    "expected_turn_around_time": {
        "id": 138,
        "test_type_id": 35,
        "value": "2",
        "unit": "Hours"
    },
    "status_trail": [
        {
            "id": 55,
            "test_id": 25,
            "status_id": 2,
            "created_date": "2024-12-06T06:42:09.321Z",
            "status": {
                "id": 2,
                "name": "pending"
            },
            "initiator": {
                "username": "hop",
                "first_name": "hop",
                "last_name": "hop"
            },
            "status_reason": {}
        }
    ],
    "order_status_trail": [
        {
            "id": 26,
            "test_id": 15,
            "status_id": 9,
            "created_date": "2024-12-06T06:42:09.256Z",
            "status": {
                "id": 9,
                "name": "specimen-not-collected"
            },
            "initiator": {
                "username": "hop",
                "first_name": "hop",
                "last_name": "hop"
            },
            "status_reason": {}
        }
    ],
    "suscept_test_result": [],
    "culture_observation": [],
    "oerr_identifiers": {
        "id": 15,
        "order_id": 15,
        "test_id": 25,
        "npid": "0D6UGE",
        "facility_section_id": 44,
        "requested_by": "maganga",
        "doc_id": None,
        "test_type_id": 35,
        "sample_collected_at": 1733385222,
        "is_panel": False
    }
}
'
"""


