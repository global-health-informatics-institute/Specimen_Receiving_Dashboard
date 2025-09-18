from extensions.extensions import db, application_config
from sqlalchemy import func

class AuthToken(db.Model):
    """"instance of every running test"""
    __tablename__ = 'auth_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auth_token = db.Column(db.String(255), nullable=False, info={"description": "Authentication token for API access"})
    issued_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.now(),
        info={"description": "Timestamp when the token was issued"}
    )
    expires_at = db.Column(
        db.DateTime,
        nullable=False,
        info={"description": "Timestamp when the token expires"}
    )
    department_id = db.Column(
        db.String(10),
        nullable=False,
        default=application_config["department_id"],
        unique=False,
        index=True
    )
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
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f'<Token lifetime (issued={self.issued_at}, expires={self.expires_at}) >'
