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
        server_default=db.text('CURRENT_TIMESTAMP'),
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
    )
    status = db.Column(db.Integer, nullable=False, index=True, default=1)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.text('CURRENT_TIMESTAMP'),
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.text('CURRENT_TIMESTAMP'),
        onupdate=db.text('CURRENT_TIMESTAMP'),
    )

    def __repr__(self) -> str:
        return f'<Token lifetime (issued={self.issued_at}, expires={self.expires_at}) >'
