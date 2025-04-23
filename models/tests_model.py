from extensions.extensions import db, dt


class Test(db.Model):
    """"instance of every running test"""
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    test_accession_id = db.Column(db.String(50), nullable=True, index=True, info={'Description':'in the table specimens, they reference tests with assession ids'})
    test_test_type = db.Column(db.String(10), nullable = True,  index = True, info={'Description':'With the reference of test_definitions, the numeric representation of ongoinga test'})
    test_test_status = db.Column(db.String(100), nullable=True, index=True, info={'Description':'Single digits to represent the status for each test for the dashboard'})
    status = db.Column(db.Integer, nullable = False, index=True, default=1, info={'Description':'This can be used to easily trash data'})
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=dt.now, index=True)
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=dt.now, onupdate=dt.now, index=True, info={'Description': 'used inplace of write_time'})
    
    def __repr__(self) -> str:
        return f'<test (id={self.id}) - (accession_id={self.test_accession_id})>'