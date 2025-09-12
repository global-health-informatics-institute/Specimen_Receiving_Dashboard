from sqlalchemy import func
from extensions.extensions import db


class Test_Definition(db.Model):
    "From the table test_types"
    __tablename__ = 'test_definitions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    test_id = db.Column(db.String(10), nullable=False, unique=True, index=True, info={"description": "In the iBlis database, an ordered test is represented as an Int. 39"})
    test_name = db.Column(db.String(100), nullable=True, index=True, info={"description":"Test full name. Prothrombin Time"})
    test_short_name = db.Column(db.String(100), nullable=True, index=True, info={"description":"Test short name as abbreviated. PT"})
    target_tat = db.Column(db.String(20), nullable = True, index = True, info={"description":"Predefined Target TATs. 2hrs"})
    test_department_id = db.Column(db.String(100), nullable=True, index=True, info={"Future implementations which reference the department a test is conducted"})
    test_definition_status = db.Column(db.Integer, nullable = False, index=True, default=1)
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
        return f'<Test difinition (id={self.id})>'