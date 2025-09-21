from flask import Request
from app import app
from extensions.extensions import logger
from services.fetch_tests_service import fetch_test_batch
from services.save_entries_service import save_entries
from werkzeug.test import EnvironBuilder

if __name__ == '__main__':
    with app.app_context():
        try:
            # get batch
            payload = fetch_test_batch()


            # Extract the data items
            data = payload.get("data")
            payload = { "data" : data }



            # push batch
            if payload:
                builder = EnvironBuilder(method='POST', json=payload)
                env = builder.get_environ()
                req = Request(env)
                if save_entries(req):
                    logger.info("daemon to fetch and push tests run succeffuly")
            else:
                logger.warning("No data to load.")
            
        except Exception as e:
            logger.error(f"error occured while feeding data: {e}")

