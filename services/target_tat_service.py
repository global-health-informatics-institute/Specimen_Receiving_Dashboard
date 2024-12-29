import app
from extensions.extensions import db, logger
from config.application import application_config
from models.test_definitions_model import Test_Definition

def all_target_tat(key):
    _test_type_ids = {
        1: application_config["test_short_name"]["test_type_1"],
        2: application_config["test_short_name"]["test_type_2"],
        3: application_config["test_short_name"]["test_type_3"],
        4: application_config["test_short_name"]["test_type_4"],
    }
    test_type = _test_type_ids.get(key)
    try:
        tat_value = db.session.query(Test_Definition).filter(
            Test_Definition.test_short_name == test_type
        ).first()
        return tat_value.target_tat
    except Exception as e:
        logger.error(f"Could'nt return TAT for {test_type}: {e}")

      
def tat_test_type_1():
    return all_target_tat(1)

def tat_test_type_2():
    return all_target_tat(2)

def tat_test_type_3():
     return all_target_tat(3)

def tat_test_type_4():
     return all_target_tat(4)

app = app.create_app()
if __name__ == "__main__":
    with app.app_context():
        print(tat_test_type_1())
        print(tat_test_type_2())
        print(tat_test_type_3())
        print(tat_test_type_4())
        
