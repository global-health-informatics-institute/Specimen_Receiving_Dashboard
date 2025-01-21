from flask import render_template, Blueprint
from scripts.serve_static_script import serve_static
from models.test_definitions_model import Test_Definition
from models.department_model import Department
from models.monthly_count_model import Monthly_Count
from models.weekly_count_model import Weekly_Count
from models.tests_model import Test
from models.status_definitions_model import Test_Status_Definition
dashboard_bp = Blueprint('dashboard', __name__)
@dashboard_bp.route('/', methods=['GET'])
def render_dashboard():

    static_data = serve_static() or {}
    def ensure_dictionary(data):
        return data if isinstance(data, dict) else {}
    
    static_data = ensure_dictionary(static_data)
    
    return render_template(
        'children/child.dashboard.html',
        static_data = serve_static(),
    )

@dashboard_bp.route('/pre_populate', methods=['GET'])
def pre_populate_route():
    ""
    # populate_department_definitions()


# @dashboard_bp.route('/dashboard', methods=['GET'])
# def render_dashboard():
#     return render_template(
#         'children/child.dashboard.html',
#     )


# @dashboard_bp.route('/load_endtries', methods=['GET'])
# def render_entries():
#     return render_template(
#         'children/child.dashboard.html',
#     )