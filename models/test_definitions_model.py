from extensions.extensions import db, dt


class Test_Definition(db.Model):
    "From the table test_types"
    __tablename__ = 'test_definitions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    test_definition_test_id = db.Column(db.String(10), nullable=False, unique=True, index=True, info={"description": "In the iBlis database, an ordered test is represented as an Int. 39"})
    test_definition_test_name = db.Column(db.String(100), nullable=True, index=True, info={"description":"Test full name. Prothrombin Time"})
    test_definition_test_short_name = db.Column(db.String(100), nullable=True, index=True, info={"description":"Test short name as abbreviated. PT"})
    test_definition_target_tat = db.Column(db.Integer, nullable = False, index = True, info={"description":"Predefined Target TATs. 2hrs"})
    test_definition_status = db.Column(db.Integer, nullable = False, index=True, default=1)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=dt.now, index=True)
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=dt.now, onupdate=dt.now, index=True)
    
    def __repr__(self) -> str:
        return f'<Test difinition (id={self.id})>'