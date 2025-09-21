from extensions.extensions import db
from sqlalchemy import func


class Test_Status_Definition(db.Model):
    """an extraction for development easy understanding"""
    """This data is a logical connection form 'specimen_statuses', 'test_statuses'"""
    __tablename__ = 'test_status_definitions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_id = db.Column(db.String(100), nullable=True, index=True, info={'Description':'counter for status meaning'})
    status_meaning = db.Column(db.String(100), nullable = True,  index = True, info={'Description':'My definition of the combination of test_status_id amd specimen_status_id will mean'})
    test_status_id = db.Column(db.String(100), nullable=True, index=True, info={'Description':'tests exists in 3 status despite each state'})
    test_status_meaning = db.Column(db.String(100), nullable = False, index = True, info={'Description':'Definition of each test status, its not enough infomation but the combination of logic, and these basics can help'})
    specimen_status_id = db.Column(db.Integer, nullable = False, index=True, default=2, info={'Description' : 'In each of the test statuses the specimen is on received status. 2'})
    specimen_status_meaning = db.Column(db.String(100), nullable = False, index=True)
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
    
    def __repr__(self) :
        return f'<test_status_definitions (id={self.id})>'