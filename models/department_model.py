from extensions.extensions import db, dt
from sqlalchemy import func


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_id = db.Column(db.String(10), nullable=False, unique=True, index=True)
    department_name = db.Column(db.String(100), nullable=True, index=True)
    department_status = db.Column(db.Integer, nullable = False, index=True, default=1)
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
        return f'<department (id={self.id}, brand={self.department_name})>'
