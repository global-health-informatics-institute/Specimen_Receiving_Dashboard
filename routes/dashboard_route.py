from flask import jsonify, render_template, Blueprint
from scripts.serve_static_script import serve_static
from services.average_service import all_tat_average
from services.current_service import all_current
from services.monthly_count_service import get_monthly_counter_values
from services.summary_service import  all_summary_counts
from services.target_tat_service import all_tat
from services.tests_service import  all_test_counts
from services.weekly_count_service import get_weekly_counter_values
dashboard_bp = Blueprint('dashboard', __name__)
@dashboard_bp.route('/', methods=['GET'])
def render_dashboard():

    static_data = serve_static() or {}
    side_bar_data = all_summary_counts() or {}
    all_test_count_data = all_test_counts() or {}
    all_tat_data = all_tat() or {}
    all_current_data = all_current()
    all_tat_average_data = all_tat_average()


    def ensure_dictionary(data):
        return data if isinstance(data, dict) else {}


    static_data = ensure_dictionary(static_data)
    side_bar_data = ensure_dictionary(side_bar_data)
    all_test_count_data = ensure_dictionary(all_test_count_data)
    all_tat_data = ensure_dictionary(all_tat_data)
    all_current_data = ensure_dictionary(all_current_data)
    all_tat_average_data = ensure_dictionary(all_tat_average_data)

    return render_template(
        'children/child.dashboard.html',
        static_data = static_data,
        side_bar_data = side_bar_data,
        all_test_count_data = all_test_count_data,
        all_tat_data = all_tat_data,
        all_current_data = all_current_data,
        all_tat_average_data = all_tat_average_data
    )


@dashboard_bp.route('/side_bar_data', methods=['GET'])
def side_bar_data():
    side_bar_data = all_summary_counts() or {}
    return jsonify(side_bar_data)


@dashboard_bp.route('/test_data_1', methods=['GET'])
def test_data_1():
    def ensure_dictionary(data):
        return data if isinstance(data, dict) else {}
    
    test_data = ensure_dictionary(all_test_counts())
    
    test_type_1_values = {
        'registered_1': test_data['registered']['registered_test_type_1'],
        'received_1': test_data['received']['received_test_type_1'],
        'in_progress_1': test_data['in_progress']['in_progress_test_type_1'],
        'pending_auth_1': test_data['pending_auth']['pending_auth_test_type_1'],
        'completed_1': test_data['completed']['completed_test_type_1'],
        'rejected_1': test_data['rejected']['rejected_test_type_1']
    }

    
    return test_type_1_values


@dashboard_bp.route('/test_data_2', methods=['GET'])
def test_data_2():
    def ensure_dictionary(data):
        return data if isinstance(data, dict) else {}
    
    test_data = ensure_dictionary(all_test_counts())
    
    test_type_2_values = {
        'registered_2': test_data['registered']['registered_test_type_2'],
        'received_2': test_data['received']['received_test_type_2'],
        'in_progress_2': test_data['in_progress']['in_progress_test_type_2'],
        'pending_auth_2': test_data['pending_auth']['pending_auth_test_type_2'],
        'completed_2': test_data['completed']['completed_test_type_2'],
        'rejected_2': test_data['rejected']['rejected_test_type_2']
    }
    
    return test_type_2_values



@dashboard_bp.route('/test_data_3', methods=['GET'])
def test_data_3():
    def ensure_dictionary(data):
        return data if isinstance(data, dict) else {}
    
    test_data = ensure_dictionary(all_test_counts())
    
    test_type_3_values = {
        'registered_3': test_data['registered']['registered_test_type_3'],
        'received_3': test_data['received']['received_test_type_3'],
        'in_progress_3': test_data['in_progress']['in_progress_test_type_3'],
        'pending_auth_3': test_data['pending_auth']['pending_auth_test_type_3'],
        'completed_3': test_data['completed']['completed_test_type_3'],
        'rejected_3': test_data['rejected']['rejected_test_type_3']
    }
    return test_type_3_values


@dashboard_bp.route('/test_data_4', methods=['GET'])
def test_data_4():
    def ensure_dictionary(data):
        return data if isinstance(data, dict) else {}
    
    test_data = ensure_dictionary(all_test_counts())
    
    test_type_4_values = {
        'registered_4': test_data['registered']['registered_test_type_4'],
        'received_4': test_data['received']['received_test_type_4'],
        'in_progress_4': test_data['in_progress']['in_progress_test_type_4'],
        'pending_auth_4': test_data['pending_auth']['pending_auth_test_type_4'],
        'completed_4': test_data['completed']['completed_test_type_4'],
        'rejected_4': test_data['rejected']['rejected_test_type_4']
    }
    return test_type_4_values


@dashboard_bp.route('/weekly_summary_data', methods=['GET'])
def weekly_summary_data():
    return get_weekly_counter_values()



@dashboard_bp.route('/monthly_summary_data', methods=['GET'])
def monthly_summary_data():
    return get_monthly_counter_values()
    
