from extensions.extensions import db, logger
from models.monthly_count_model import Monthly_Count


COLUMN_MAPPING = {
    1: "monthly_count_registered",
    2: "monthly_count_received",
    3: "monthly_count_progress",
    4: "monthly_count_pending",
    5: "monthly_count_complete",
    0: "monthly_count_rejected",
}
table = Monthly_Count

def monthly_increment(department_id, status):
        column_name =  COLUMN_MAPPING.get(status)
        try:
            result = db.session.query(table).filter_by(department_id=department_id).update(
                {column_name: table.__table__.c[column_name] + 1},
            )
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error during incrementing: {e}")

def weekly_decrement(department_id, status):
        column_name =  COLUMN_MAPPING.get(status)
        try:
            result = db.session.query(table).filter_by(department_id=department_id).update(
                {column_name: db.case([(table.__table__.c[column_name] > 0, table.__table__.c[column_name] - 1)], else_=0)},
            )
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error during decrementing: {e}")
