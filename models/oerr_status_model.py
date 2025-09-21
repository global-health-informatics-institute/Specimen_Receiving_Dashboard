from extensions.extensions import db, dt


class OERR_Status_Definition(db.Model):
    """an extraction for oerr implementatiom easy understanding"""
    """Based on the implementation of using the OERR to provide test objects"""
    __tablename__ = 'oerr_status_definition'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oerr_status_id = db.Column(db.String(100), nullable=True, index=True, info={'Description':'possible status value'})
    oerr_status_meaning = db.Column(db.String(100), nullable = True,  index = True, info={'Description ':'String representation of the status_id'})
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=dt.now, index=True)
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=dt.now, onupdate=dt.now, index=True)
    def __repr__(self) :
        return f'<oerr_status_id (id={self.id})>'