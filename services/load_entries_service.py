from sqlalchemy import func, case
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models.config import testType1, testType2, testType3, testType4, interval, time_out
from models import Test, WeeklySummary, MonthlySummary  # Example models, adjust as needed
from extensions import iblis_engine, srs_engine  # SQLAlchemy engines

# Helpers
def get

# Define constants
intvl = interval  # e.g., 1
department_id = getDepartmentIdHelper()
test_type_ids = [getTestTypeID(testType1), getTestTypeID(testType2), getTestTypeID(testType3), getTestTypeID(testType4)]

# Create session factories
IblisSession = sessionmaker(bind=iblis_engine)
SrsSession = sessionmaker(bind=srs_engine)

# Helper functions for updating weekly and monthly summaries
def _update_summary(session, table, status):
    """Helper to update weekly or monthly summaries."""
    column_name = case(
        [
            (status == 2, table.weekly_registered),
            (status == 0, table.weekly_received),
            (status == 3, table.weekly_progress),
            (status == 4, table.weekly_pending),
            (status == 5, table.weekly_complete),
        ]
    )

    session.query(table).filter_by(id=1).update({column_name: column_name + 1})

def load_entries():
    try:
        # Open database sessions
        iblis_session = IblisSession()
        srs_session = SrsSession()

        # Query for the latest tests from iBlissDB
        tests_query = (
            iblis_session.query(
                Test.accession_number.label("accession_id"),
                Test.test_type_id.label("test_type"),
                Test.test_status_id.label("test_status"),
                func.row_number().over(
                    partition_by=(Test.accession_number, Test.test_type_id),
                    order_by=Test.time_created.desc()
                ).label("rn")
            )
            .join(Specimen, Test.specimen_id == Specimen.id)
            .filter(
                Specimen.time_accepted.isnot(None),
                Specimen.specimen_type_id == department_id,
                Test.test_status_id.notin_([1, 6, 7, 8]),
                Test.time_created >= func.current_date() + func.interval(f"{time_out} HOUR"),
                Test.time_created <= func.current_date() + func.interval(f"{intvl} DAY") + func.interval(f"{time_out} HOUR"),
                Test.test_type_id.in_(test_type_ids),
            )
            .subquery()
        )

        latest_tests = (
            iblis_session.query(tests_query.c.accession_id, tests_query.c.test_type, tests_query.c.test_status)
            .filter(tests_query.c.rn == 1)
            .all()
        )

        # Process each result and update srsDB
        for test in latest_tests:
            accession_id, test_type, test_status = test.accession_id, test.test_type, test.test_status

            # Check if the record already exists in srsDB
            existing_test = (
                srs_session.query(Test)
                .filter(and_(Test.accession_id == accession_id, Test.test_type == test_type))
                .first()
            )

            if not existing_test:
                # Insert new record if not found
                new_test = Test(
                    accession_id=accession_id,
                    test_type=test_type,
                    test_status=test_status,
                )
                srs_session.add(new_test)
                _update_summary(srs_session, WeeklySummary, test_status)
                _update_summary(srs_session, MonthlySummary, test_status)
                print(f"Condition 1: Inserted new record for accession_id: {accession_id}, test_type: {test_type}, test_status: {test_status}")
            else:
                existing_status = existing_test.test_status
                # Skip if existing status = 0 and new status is 1 or 2
                if existing_status == 0 and test_status in [1, 2]:
                    continue
                # Update the record if statuses are different
                elif existing_status != test_status:
                    existing_test.test_status = test_status
                    _update_summary(srs_session, WeeklySummary, test_status)
                    _update_summary(srs_session, MonthlySummary, test_status)
                    print(f"Updated record for accession_id: {accession_id}, test_type: {test_type}, new test_status: {test_status}, old test_status: {existing_status}")

        # Commit the changes to srsDB
        srs_session.commit()

    except SQLAlchemyError as e:
        print(f"Error: {e}")
    finally:
        # Close database sessions
        iblis_session.close()
        srs_session.close()
