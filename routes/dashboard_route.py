from flask import render_template, Blueprint

from services.serve_static_service import serve_static

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