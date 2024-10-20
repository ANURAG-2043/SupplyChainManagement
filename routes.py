from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import  create_refresh_token, create_access_token, jwt_required, get_jwt_identity

dashboard_bp = Blueprint('dashboard', __name__)

# @dashboard_bp.route('/orders')
# def orders():
#     return render_template('orders.html')

@dashboard_bp.route('/inventory')
def inventory():
    return render_template('inventory.html')

# @dashboard_bp.route('/transportation')
# def reports():
#     return render_template('transportation.html')

@dashboard_bp.route('/analytics')
def analytics():
    return render_template('analytics.html')

@dashboard_bp.route('/visualization')
def visualization():
    return render_template('visualization.html')
