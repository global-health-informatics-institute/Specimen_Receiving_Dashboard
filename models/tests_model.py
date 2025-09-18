from extensions.extensions import db
from sqlalchemy import func

class Test(db.Model):
    """"instance of every running test"""
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    test_accession_id = db.Column(db.String(50), nullable=True, index=True)
    test_test_type = db.Column(db.String(10), nullable=True, index=True)
    test_test_status = db.Column(db.String(100), nullable=True, index=True)
    status = db.Column(db.Integer, nullable=False, index=True, default=1)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.now(),
        index=True
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.text('CURRENT_TIMESTAMP'),
        onupdate=db.text('CURRENT_TIMESTAMP'),
        index=True
    )

    def __repr__(self) -> str:
        return f'<Test (id={self.id}) - (accession_id={self.test_accession_id})>'
