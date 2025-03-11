from flask import jsonify, render_template, Blueprint
from scripts.serve_static_script import serve_static
from services.current_service import all_current
from services.summary_service import  all_summary_counts
from services.target_tat_service import all_tat
from services.tests_service import  all_test_counts
dashboard_bp = Blueprint('dashboard', __name__)
@dashboard_bp.route('/', methods=['GET'])
def render_dashboard():

    static_data = serve_static() or {}
    side_bar_data = all_summary_counts() or {}
    all_test_count_data = all_test_counts() or {}
    all_tat_data = all_tat() or {}
    all_current_data = all_current()


    def ensure_dictionary(data):
        return data if isinstance(data, dict) else {}


    static_data = ensure_dictionary(static_data)
    side_bar_data = ensure_dictionary(side_bar_data)
    all_test_count_data = ensure_dictionary(all_test_count_data)
    all_tat_data = ensure_dictionary(all_tat_data)
    all_current_data = ensure_dictionary(all_current_data)

    return render_template(
        'children/child.dashboard.html',
        static_data = static_data,
        side_bar_data = side_bar_data,
        all_test_count_data = all_test_count_data,
        all_tat_data = all_tat_data,
        all_current_data = all_current_data
    )


@dashboard_bp.route('/side_bar_data', methods=['GET'])
def side_bar_data():
    side_bar_data = all_summary_counts() or {}
    return jsonify(side_bar_data)
