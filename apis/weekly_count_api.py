from extensions.extensions import db,logger
from models.weekly_count_model import Weekly_Count


COLUMN_MAPPING = {
    1: "weekly_count_registered",
    2: "weekly_count_received",
    3: "weekly_count_progress",
    4: "weekly_count_pending",
    5: "weekly_count_complete",
    0: "weekly_count_rejected",
}
table = Weekly_Count

def weekly_increment(department_id, status):
        column_name =  COLUMN_MAPPING.get(status)
        try:
            result = db.session.query(table).filter_by(department_id=department_id).update(
                {column_name: table.__table__.c[column_name] + 1},
                synchronize_session=False
            )
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error during incrementing: {e}")

def weekly_decrement(department_id, test_id, status):
        column_name =  COLUMN_MAPPING.get(status)
        try:
            result = db.session.query(table).filter_by(department_id=department_id).update(
                {column_name: db.case([(table.__table__.c[column_name] > 0, table.__table__.c[column_name] - 1)], else_=0)},
            )
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error during decrementing: {e}")
