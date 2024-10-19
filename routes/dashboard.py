from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__)

# Route to render the dashboard page
@dashboard_bp.route('/')
def dashboard_home():
    return render_template('dashboard.html')

# Route to render the orders page
# @dashboard_bp.route('/orders')
# def order_page():
#     return render_template('orders.html')

# Route to render the inventory page
@dashboard_bp.route('/inventory')
def inventory_page():
    return render_template('inventory.html')

# Route to render the reports page
@dashboard_bp.route('/reports')
def reports_page():
    return render_template('reports.html')

# Route to render the analytics page
@dashboard_bp.route('/analytics')
def analytics_page():
    return render_template('analytics.html')

# Route to render the visualization page
@dashboard_bp.route('/visualization')
def visualization_page():
    return render_template('visualization.html')
