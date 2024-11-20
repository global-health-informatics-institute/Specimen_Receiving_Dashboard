from flask import render_template, Blueprint

from services.pre_populate_service import populate_department_definitions
from services.serve_static_service import serve_static
from models.status_definitions_model import Test_Status_Definition
from models.department_model import Department
dashboard_bp = Blueprint('dashboard', __name__)
@dashboard_bp.route('/', methods=['GET'])
def render_dashboard():
    static_data = serve_static() or {}
    def ensure_dictionary(data):
        return data if isinstance(data, dict) else {}
    static_data = ensure_dictionary(static_data)
    print(static_data)
    return render_template(
        'children/child.dashboard.html',
        static_data = static_data,
    )

@dashboard_bp.route('/pre_populate', methods=['GET'])
def pre_populate_route():
    populate_department_definitions()