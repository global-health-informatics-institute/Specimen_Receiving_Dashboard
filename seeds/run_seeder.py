from extensions.extensions import logger
from seeds.departmet_seeder import run_department_seeder
from seeds.monthly_summary_seeder import run_monthly_count_seeder
from seeds.status_definitions_seeder import run_test_status_definitions_seeder
from seeds.test_type_seeder import run_test_type_Seeder
from seeds.weekly_summary_seeder import run_weekly_count_seeder


if __name__ == "__main__":
    logger.info(run_department_seeder())
    logger.info(run_test_type_Seeder())
    logger.info(run_monthly_count_seeder())
    logger.info(run_weekly_count_seeder())
    logger.info(run_test_status_definitions_seeder())