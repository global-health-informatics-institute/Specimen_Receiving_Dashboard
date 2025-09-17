from datetime import date, datetime

from flask import json, jsonify
from services.weekly_increment_service import weekly_increment as weekly_increment_api
from services.monthly_increment_service import monthly_increment as monthly_increment_api
from extensions.extensions import logger, db, STATUS_NEW, STATUS_VOIDED, DEPARTMENT_ID
from models.tests_model import Test
from services.process_payload import process_payload
from sqlalchemy.exc import SQLAlchemyError

department_id  = DEPARTMENT_ID
def save_entries(payload):
    results = []
    count = 0
    try:
        # ---------- Validate request ----------
        if not payload.is_json:
            logger.error("Invalid request, JSON data is required")
            return {
                "error": "Invalid request, JSON data is required",
                "status" : 415
                } 

        items = payload.get_json()

        if not items or "data" not in items:
            logger.error("Missing 'data' key in JSON")
            return {
                "message": "Invalid or missing JSON data",
                "status" : 400
                }

        # ---------- Process each item ----------
        for idx, record in enumerate(items["data"], start=1):
            accession_number, test_status, test_type, department_id, created_date = process_payload(record)

            # --- Field checks ---
            if not accession_number:
                results.append({f"item-{idx}": {"warning": "Missing accession_number", "status": 400}})
                continue
            if test_status is None:
                results.append({f"item-{idx}": {"warning": "Missing test_status", "status": 400}})
                continue
            if not test_type:
                results.append({f"item-{idx}": {"warning": "Missing test_type", "status": 400}})
                continue
            if not department_id:
                results.append({f"item-{idx}": {"warning": "Missing department_id", "status": 400}})
                continue
            if not created_date:
                results.append({f"item-{idx}": {"warning": "Missing created_date", "status": 400}})
                continue
            
            # --- clean off old test ---
            if datetime.fromisoformat(created_date).date() != date.today():
                results.append({f"item-{idx}": {"warning": "Test not within Today", "status": 400}})
                continue

            

            # --- DB lookups ---
            existing_test = db.session.query(Test).filter_by(
                test_accession_id=accession_number,
                test_test_type=test_type
            ).first()

            unchanged_test = db.session.query(Test).filter_by(
                test_test_status=test_status,
                test_accession_id=accession_number,
                test_test_type=test_type
            ).first()

            if existing_test:
                if int(existing_test.test_test_status) in [0, 9]:
                    results.append({f"item-{idx}": {
                        "warning": "Test is voided or cancelled, no updates allowed",
                        "status": 403
                    }})
                    continue

                if unchanged_test:
                    results.append({f"item-{idx}": {
                        "warning": "Test already exists with the same status",
                        "status": 304
                    }})
                    continue

                # Update status (handles skipped statuses too)
                
                if int(existing_test.test_test_status) + 1 == int(test_status) or int(test_status) == 0:
                    # with no skips
                    db.session.query(Test).filter_by(
                        test_accession_id=accession_number
                    ).update({"test_test_status": str(test_status)})
                    weekly_increment_api(department_id, test_status)
                    monthly_increment_api(department_id, test_status)
                else:
                    # with skips
                    diff = test_status - int(existing_test.test_test_status)
                    while diff > 0:
                        weekly_increment_api(department_id, test_status - (diff - 1))
                        monthly_increment_api(department_id, test_status - (diff - 1))
                        diff -= 1
                    db.session.query(Test).filter_by(
                        test_accession_id=accession_number
                    ).update({"test_test_status": test_status})

                logger.info(f"Updated existing test {accession_number}")
            else:
                # ---------- New test ----------
                new_test = Test(
                    test_test_status=test_status,
                    test_accession_id=accession_number,
                    test_test_type=test_type
                )
                db.session.add(new_test)

                if test_status == STATUS_NEW:
                    weekly_increment_api(department_id, test_status)
                    monthly_increment_api(department_id, test_status)

                elif test_status == STATUS_VOIDED:
                    weekly_increment_api(department_id, test_status)
                    monthly_increment_api(department_id, test_status)
                    weekly_increment_api(department_id, 1)
                    monthly_increment_api(department_id, 1)
                else:
                    i = test_status
                    while i > 0:
                        weekly_increment_api(department_id, i)
                        monthly_increment_api(department_id, i)
                        i -= 1
                logger.info(f"Added new test {accession_number}")

            # --------- update on success --------
            count += 1
            results.append(
                {f"item-{idx}": {"status": "processed"}})

        # ---------- Commit & return ----------
        db.session.commit()
        logger.info(
                json.dumps(
                    {
                        "processed_count": count,
                        "save_count": idx,
                        "results": results
                    }, indent=2
                )
            )
        return {
            "processed_count": count,
            "results": results
        }

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error: {e}")
        return ({
            "error": "An error occurred while saving the entries",
            "status" : 500
            })

    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error: {e}")
        return {
            "error": "An unexpected error occurred",
            "status" : 500
        }
