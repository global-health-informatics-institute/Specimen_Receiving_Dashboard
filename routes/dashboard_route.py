from flask import jsonify, render_template, Blueprint
from scripts.serve_static_script import serve_static
from services.summary_service import all_counts
dashboard_bp = Blueprint('dashboard', __name__)
@dashboard_bp.route('/', methods=['GET'])
def render_dashboard():

    def ensure_dictionary(data):
        return data if isinstance(data, dict) else {}

    static_data = serve_static() or {}
    side_bar_data = all_counts() or {}


    static_data = ensure_dictionary(static_data)
    side_bar_data = ensure_dictionary(side_bar_data)
    return render_template(
        'children/child.dashboard.html',
        static_data = serve_static(),
        side_bar_data = all_counts(),
    )


@dashboard_bp.route('/side_bar_data', methods=['GET'])
def side_bar_data():
    side_bar_data = all_counts() or {}
    return jsonify(side_bar_data)
