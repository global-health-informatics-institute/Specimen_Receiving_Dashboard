from extensions.extensions import db, dt
from sqlalchemy import func


class Lab_Location(db.Model):
    __tablename__ = 'lab_locations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lab_location_id = db.Column(db.String(10), nullable=False, unique=True, index=True)
    lab_location_name = db.Column(db.String(100), nullable=True, index=True)
    lab_location_status = db.Column(db.Integer, nullable = False, index=True, default=1)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.text('CURRENT_TIMESTAMP'),
        index=True
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.text('CURRENT_TIMESTAMP'),
        onupdate=db.text('CURRENT_TIMESTAMP'),
        index=True
    )
    
    def __repr__(self):
        return f'<lab_location (id={self.id}, name={self.lab_location_name})>'
