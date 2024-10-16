from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from blockchain_integration import create_order, get_order, update_order_status

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For managing session

# Role-based dashboard views
@app.route('/dashboard')
def dashboard():
    if 'role' not in session:
        return redirect(url_for('login'))  # Redirect to login if no role

    role = session['role']
    if role == 'consumer':
        # Render consumer dashboard
        return render_template('consumer_dashboard.html')
    elif role == 'seller':
        # Render seller dashboard
        return render_template('seller_dashboard.html')
    else:
        return jsonify({"error": "Invalid role"}), 403

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    role = data.get('role')  # Get role (consumer/seller) from request
    session['role'] = role  # Save role in session
    return redirect(url_for('dashboard'))  # Redirect to the appropriate dashboard

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/create_order', methods=['POST'])
def create_new_order():
    if 'role' not in session or session['role'] != 'seller':
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    order_id = data['orderId']
    manufacturer_id = data['manufacturerId']
    product_details = data['productDetails']
    response = create_order(order_id, manufacturer_id, product_details)
    return jsonify({"status": "Order Created", "response": response})

@app.route('/get_order/<order_id>', methods=['GET'])
def fetch_order(order_id):
    if 'role' not in session:
        return jsonify({"error": "Unauthorized"}), 403

    order = get_order(order_id)
    return jsonify(order)

@app.route('/update_order', methods=['POST'])
def update_order():
    if 'role' not in session or session['role'] != 'seller':
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    order_id = data['orderId']
    status = data['status']
    response = update_order_status(order_id, status)
    return jsonify({"status": "Order Updated", "response": response})

if __name__ == '__main__':
    app.run(debug=True)
