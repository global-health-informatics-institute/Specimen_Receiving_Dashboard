"""
This script resets the weekly counts for all departments.
to be run with a systemd service:
    reset_weekly_counts.service
    TODO: create reset_weekly_counts.service script
    TODO: create timer reset_weekly_counts.timer
    TODO: implement proper reset weekly counter logic
"""
from extensions.extensions import db, department_data, logger
from models.weekly_count_model import Weekly_Count
from app import app

def reset_weekly():
    """Reset the weekly counts for all departments."""
    with app.app_context():
        db.session.query(Weekly_Count).update({
            "weekly_count_registered": 0,
            "weekly_count_received": 0,
            "weekly_count_progress": 0,
            "weekly_count_pending": 0,
            "weekly_count_complete": 0,
            "weekly_count_rejected": 0
        })
        db.session.commit()