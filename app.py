from flask import Blueprint, Flask, render_template, jsonify, request
from routes.dashboard import dashboard_bp
from flask_socketio import SocketIO
from web3 import Web3
import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
import os

app = Flask(__name__)
socketio = SocketIO(app)

 # Register blueprints
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
dashboard_bp = Blueprint('dashboard', __name__)
# order_bp = Blueprint('order', __name__)

w3 = Web3(Web3.HTTPProvider(os.getenv('https://sepolia.infura.io/v3/d4aa7e5dd36c40e8a7b134954fa4c8c9')))  # Use environment variable
contract_address = os.getenv('0x2848B7f1693BBD077aF0F7F4f9d2C5B71B8D944e') 

contract_abi = [{
        "inputs": [
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "string", "name": "description", "type": "string"},
            {"internalType": "string", "name": "productType", "type": "string"},
            {"internalType": "uint256", "name": "price", "type": "uint256"},
            {"internalType": "string", "name": "location", "type": "string"},
            {"internalType": "string", "name": "shippingCarrier", "type": "string"},
            {"internalType": "string", "name": "customerDemographics", "type": "string"}
        ],
        "name": "addProduct",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "sku", "type": "uint256"},
            {"internalType": "string", "name": "feedback", "type": "string"},
            {"internalType": "uint8", "name": "rating", "type": "uint8"}
        ],
        "name": "addReview",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "sku", "type": "uint256"},
            {"internalType": "uint256", "name": "revenue", "type": "uint256"}
        ],
        "name": "logRevenue",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "sku", "type": "uint256"},
            {"internalType": "uint256", "name": "revenue", "type": "uint256"}
        ],
        "name": "markAsSold",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "sku", "type": "uint256"},
            {"indexed": False, "internalType": "address", "name": "previousOwner", "type": "address"},
            {"indexed": False, "internalType": "address", "name": "newOwner", "type": "address"},
            {"indexed": False, "internalType": "string", "name": "newLocation", "type": "string"}
        ],
        "name": "OwnershipTransferred",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "sku", "type": "uint256"},
            {"indexed": False, "internalType": "string", "name": "name", "type": "string"},
            {"indexed": False, "internalType": "string", "name": "description", "type": "string"},
            {"indexed": False, "internalType": "string", "name": "productType", "type": "string"},
            {"indexed": False, "internalType": "address", "name": "owner", "type": "address"},
            {"indexed": False, "internalType": "string", "name": "location", "type": "string"},
            {"indexed": False, "internalType": "uint256", "name": "price", "type": "uint256"}
        ],
        "name": "ProductAdded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "sku", "type": "uint256"},
            {"indexed": False, "internalType": "address", "name": "buyer", "type": "address"}
        ],
        "name": "ProductSold",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "sku", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "revenue", "type": "uint256"}
        ],
        "name": "RevenueGenerated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "sku", "type": "uint256"},
            {"indexed": False, "internalType": "address", "name": "customer", "type": "address"},
            {"indexed": False, "internalType": "uint8", "name": "rating", "type": "uint8"},
            {"indexed": False, "internalType": "string", "name": "feedback", "type": "string"}
        ],
        "name": "ReviewAdded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "sku", "type": "uint256"},
            {"indexed": False, "internalType": "address", "name": "from", "type": "address"},
            {"indexed": False, "internalType": "address", "name": "to", "type": "address"},
            {"indexed": False, "internalType": "string", "name": "details", "type": "string"}
        ],
        "name": "TransactionLogged",
        "type": "event"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "sku", "type": "uint256"},
            {"internalType": "address", "name": "newOwner", "type": "address"},
            {"internalType": "string", "name": "newLocation", "type": "string"}
        ],
        "name": "transferOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "sku", "type": "uint256"}
        ],
        "name": "getProductDetails",
        "outputs": [
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "string", "name": "description", "type": "string"},
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "bool", "name": "isSold", "type": "bool"},
            {"internalType": "uint256", "name": "revenueGenerated", "type": "uint256"},
            {"internalType": "string", "name": "location", "type": "string"},
            {"internalType": "uint256", "name": "reviewCount", "type": "uint256"},
            {"internalType": "uint256", "name": "transactionCount", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "sku", "type": "uint256"}
        ],
        "name": "getProductReviews",
        "outputs": [
            {
                "components": [
                    {"internalType": "address", "name": "customer", "type": "address"},
                    {"internalType": "string", "name": "feedback", "type": "string"},
                    {"internalType": "uint8", "name": "rating", "type": "uint8"}
                ],
                "internalType": "struct SupplyChain.Review[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "sku", "type": "uint256"}
        ],
        "name": "getTransactionHistory",
        "outputs": [
            {
                "components": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
                    {"internalType": "string", "name": "details", "type": "string"}
                ],
                "internalType": "struct SupplyChain.Transaction[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "productCount",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "name": "products",
        "outputs": [
            {"internalType": "uint256", "name": "sku", "type": "uint256"},
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "string", "name": "description", "type": "string"},
            {"internalType": "string", "name": "productType", "type": "string"},
            {"internalType": "uint256", "name": "price", "type": "uint256"},
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "string", "name": "location", "type": "string"},
            {"internalType": "bool", "name": "isSold", "type": "bool"},
            {"internalType": "uint256", "name": "revenueGenerated", "type": "uint256"},
            {"internalType": "string", "name": "shippingCarrier", "type": "string"},
            {"internalType": "string", "name": "customerDemographics", "type": "string"}
        ],
        "stateMutability": "view",
        "type": "function"
    }]  

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Load the CSV file
csv_file_path = os.getenv('CSV_FILE_PATH')
products_data = pd.read_csv('/Users/dailyAnurag/Desktop/colab_prj/SupplyChainManagement/data/sample/supply_chain_data_processed_1.csv')

#transportation model integration:
model_path = r'/Users/dailyAnurag/Desktop/colab_prj/SupplyChainManagement/ml/models/Transportation_cost_model.h5'
with open(model_path, 'rb') as f:
    model = pickle.load(f)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard/transportation', methods=['GET'])
def transportation_page():
    return render_template('transportation.html')

@app.route('/dashboard/transportation/predict', methods=['POST'])
def predict():
    # Get input from the form
    data = request.json
    sku = int(data['SKU'])
    lead_times = int(data['Lead times'])
    order_quantities = int(data['Order quantities'])
    shipping_carriers = data['Shipping carriers']
    location = data['Location']
    routes = data['Routes']
    defect_rates = float(data['Defect rates'])
    transportation_modes = data['Transportation modes']
    supplier_name = data['Supplier name']
    shipping_times = int(data['Shipping times'])
    inspection_results = data['Inspection results']
    input_data = np.array([[sku, lead_times, order_quantities, shipping_carriers, location, routes,
                            defect_rates, transportation_modes, supplier_name, shipping_times, inspection_results]])
    input_data_scaled = scaler.transform(input_data)
    prediction = model.predict(input_data_scaled)
    return jsonify({'prediction': float(prediction[0][0])})


@app.route('/dashboard/orders')
def orders():
    transactions = get_all_transactions()
    sales = get_all_sales()  
    notifications = get_notifications()
    return render_template('orders.html', transactions=transactions, sales=sales, notifications=notifications)

@app.route('/orders/transactions')
def get_transactions():
    try:
        transactions = fetch_transactions_from_blockchain()
        return render_template('transaction.html', transactions=transactions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/orders/sales')
def get_sales():
    try:
        sales = fetch_sales_from_blockchain()
        return render_template('sales.html', sales = sales)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Fetch all transactions from the blockchain
def fetch_transactions_from_blockchain():
    transactions = []
    try:
        total_transactions = contract.functions.productCount().call()  
        for i in range(total_transactions):
            transaction = contract.functions.getTransactionHistory(i).call()  
            transactions.append({
                'id': i,
                'sku': transaction[0],
                'from': transaction[1],
                'to': transaction[2],
                'timestamp': transaction[3],
                'details': transaction[4]
            })
    except Exception as e:
        print(f"Error fetching transactions: {e}")
    return transactions

def get_all_transactions():
    return fetch_transactions_from_blockchain()

# # Fetch all sales data from the blockchain and CSV
def fetch_sales_from_blockchain():
    sales = []
    try:
        total_sales = contract.functions.productCount().call()
        for i in range(total_sales):
            sale = contract.functions.getProductDetails(i).call()  
            sales.append({
                'sku': sale[0],
                'amount': sale[1],
                'revenue': sale[2],
                'timestamp': sale[3]
            })
    except Exception as e:
        print(f"Error fetching sales: {e}")
    return sales

def get_sales_from_csv():
    sales_data = []
    try:
        df = pd.read_csv('data/sample/supply_chain_data_processed_1.csv')  # Ensure this path is correct
        for index, row in df.iterrows():
            sales_data.append({
                'sku': row['sku'],  
                'amount': row['amount'],
                'revenue': row['revenue'],
                'timestamp': row['timestamp']
            })
    except Exception as e:
        print(f"Error loading sales from CSV: {e}")
    return sales_data

def get_all_sales():
    blockchain_sales = fetch_sales_from_blockchain()
    csv_sales = get_sales_from_csv()
    return blockchain_sales + csv_sales

def get_notifications():
    notifications = []
    try:
        huge_sales = contract.functions.getHugeSales().call()  
        for sale in huge_sales:
            notifications.append({
                'message': f"Huge sale recorded for SKU {sale['sku']} with revenue {sale['revenue']}"
            })
    
        low_stock_items = contract.functions.getLowStockItems().call()  
        for item in low_stock_items:
            notifications.append({
                'message': f"Low stock warning for SKU {item['sku']}, only {item['stock']} items remaining."
            })
    except Exception as e:
        print(f"Error fetching notifications: {e}")
    
    return notifications


if __name__ == '__main__':
    app.debug = True  # Enable debug mode
    # app.run(debug=True)
    socketio.run(app)
