"""
This script resets the monthly counts for all departments.
to be run with a systemd service:
    reset_monthly_counts.service
    TODO: create reset_monthly_counts.service script
    TODO: create timer reset_monthly_counts.timer
    TODO: implement proper reset monthly counter logic
"""
from extensions.extensions import db, department_data, logger
from models.weekly_count_model import Weekly_Count

def reset_monthly():
    """Reset the monthly counts for all departments."""
    with app.app_context():
        db.session.query(Weekly_Count).update({
            "monthly_count_registered": 0,
            "monthly_count_received": 0,
            "monthly_count_progress": 0,
            "monthly_count_pending": 0,
            "monthly_count_complete": 0,
            "monthly_count_rejected": 0
        })
        db.session.commit()