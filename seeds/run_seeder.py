from run import flask_app # Make sure this imports the app object from app.py (or whatever your app module is)

from extensions.extensions import logger, start_time
from seeds.departmet_seeder import run_department_seeder
from seeds.monthly_summary_seeder import run_monthly_count_seeder
from seeds.oerr_status_seeder import run_oerr_status_definitions_seeder
from seeds.status_definitions_seeder import run_test_status_definitions_seeder
from seeds.test_type_seeder import run_test_type_seeder
from seeds.weekly_summary_seeder import run_weekly_count_seeder


if __name__ == "__main__":
    with flask_app.app_context(): 
        (run_department_seeder())
        (run_test_type_seeder())
        (run_monthly_count_seeder())
        (run_weekly_count_seeder())
        (run_test_status_definitions_seeder())
        (run_oerr_status_definitions_seeder())
        