from extensions.extensions import db, dt


class Monthly_Count(db.Model):
    """"Since first day of the week Month"""
    __tablename__ = 'monthly_count'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, default=1, index=True)
    monthly_count_registered = db.Column(db.Integer, default=0, index=True)
    monthly_count_received = db.Column(db.Integer, default=0, index=True)
    monthly_count_progress = db.Column(db.Integer, default=0, index=True)
    monthly_count_pending = db.Column(db.Integer, default=0, index=True)
    monthly_count_complete = db.Column(db.Integer, default=0, index=True)
    monthly_count_rejected = db.Column(db.Integer, default=0, index=True)
    monthly_Count_status = db.Column(db.Integer, nullable = False, index=True, default=1, info={'Description':'This can be used to easily trash data'})
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=dt.now, index=True)
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=dt.now, onupdate=dt.now, index=True)
    
    def __repr__(self) -> str:
        return f'<monthly_count (id={self.id}) - (active_status={self.monthly_Count_status})>'
