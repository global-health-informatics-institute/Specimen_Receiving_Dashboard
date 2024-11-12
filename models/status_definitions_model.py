from extensions.extensions import db, dt


class Test_Status_Definition(db.Model):
    """an extraction for development easy understanding"""
    """Data is a logical connection form 'specimen_statuses', 'test_statuses'"""
    __tablename__ = 'test_status_definitions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    test_status_definition_status_id = db.Column(db.String(100), nullable=True, index=True, info={'Description':'counter for status meaning'})
    test_status_definition_status_meaning = db.Column(db.String(100), nullable = True,  index = True, info={'Description':'My definition of the combination of test_status_id amd specimen_status_id will mean'})
    test_status_definition_test_status_id = db.Column(db.String(100), nullable=True, index=True, info={'Description':'tests exists in 3 status despite each state'})
    test_status_definition_test_status_meaning = db.Column(db.String(100), nullable = False, index = True, info={'Description':'Definition of each test status, its not enough infomation but the combination of logic, and these basics can help'})
    test_status_definition_specimen_status_id = db.Column(db.Integer, nullable = False, index=True, default=2, info={'Description' : 'In each of the test statuses the specimen is on received status. 2'})
    specimen_status_meaning = db.Column(db.Integer, nullable = False, index=True, default=1)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=dt.now, index=True)
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=dt.now, onupdate=dt.now, index=True)
    
    def __repr__(self) -> str:
        return f'<test_status_definitions (id={self.id})>'