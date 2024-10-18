from flask import Blueprint, request, jsonify, render_template
# from flask_bcrypt import Bcrypt
from flask_jwt_extended import  create_refresh_token, create_access_token, jwt_required, get_jwt_identity
# import sqlite3
# import logging

# auth = Blueprint('auth', __name__)
dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/overview')
def overview():
    return render_template('overview.html')

@dashboard_bp.route('/orders')
def orders():
    return render_template('orders.html')

@dashboard_bp.route('/inventory')
def inventory():
    return render_template('inventory.html')

@dashboard_bp.route('/reports')
def reports():
    return render_template('reports.html')

@dashboard_bp.route('/analytics')
def analytics():
    return render_template('analytics.html')

@dashboard_bp.route('/visualization')
def visualization():
    return render_template('visualization.html')
