from extensions.misc import map_lims_to_oerr_dashboard_status
from extensions.extensions import DEPARTMENT_ID

DEPARTMENT_ID

def process_payload(payload):
    def actual_status(specimen_status, test_status):
        return map_lims_to_oerr_dashboard_status(test_status, specimen_status)
    
    def get_status_info():
        return actual_status(payload.get("order_status"), payload.get("status"))
    
    def get_test_type():
        return  payload.get("test_type_id")
    
    def get_accession_number():
        return  payload.get("accession_number")
    
    def get_created_date():
        return payload.get("created_date")

    test_status = get_status_info()
    test_type = get_test_type()
    accession_number = get_accession_number()
    department_id = DEPARTMENT_ID
    created_date = get_created_date()
    return accession_number, test_status, test_type, department_id, created_date
