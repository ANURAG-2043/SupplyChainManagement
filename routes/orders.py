from flask import Blueprint, render_template

order_bp = Blueprint('order', __name__)

@order_bp.route('/')
def dashboard_home():
    return render_template('orders.html')
