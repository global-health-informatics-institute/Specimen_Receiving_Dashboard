from sqlalchemy import func
from extensions.extensions import db, dt


class Weekly_Count(db.Model):
    """"Since first day of the week count"""
    __tablename__ = 'weekly_count'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    department_id = db.Column(db.Integer, index=True, info={'Description':'Changed from one row to deparment count'})
    weekly_count_registered = db.Column(db.Integer, default=0, index=True)
    weekly_count_received = db.Column(db.Integer, default=0, index=True)
    weekly_count_progress = db.Column(db.Integer, default=0, index=True)
    weekly_count_pending = db.Column(db.Integer, default=0, index=True)
    weekly_count_complete = db.Column(db.Integer, default=0, index=True)
    weekly_count_rejected = db.Column(db.Integer, default=0, index=True)
    Weekly_Count_status = db.Column(db.Integer, nullable = False, index=True, default=1, info={'Description':'This can be used to easily trash data'})
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.now(),
        index=True
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        index=True
    )

    def __repr__(self) -> str:
        return f'<weekly_count (id={self.id}) - (active_status={self.Weekly_Count_status})>'
