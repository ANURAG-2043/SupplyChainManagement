from hfc.fabric import Client
import json
import pandas as pd

# Initialize the Hyperledger Fabric client with the network profile
fabric_client = Client(net_profile="path/to/network_profile.yaml")

# Get the user for signing transactions (e.g., admin user)
admin_user = fabric_client.get_user('Org1', 'admin')

# Get the channel object for 'supplychain-channel'
channel = fabric_client.get_channel('supplychain-channel')

# Create a new order transaction
def create_order(order_id, manufacturer_id, product_details):
    try:
        # Invoke the chaincode to create a new order
        response = fabric_client.chaincode_invoke(
            requestor=admin_user,
            channel_name='supplychain-channel',
            peers=['peer0.org1.example.com'],
            args=[order_id, manufacturer_id, product_details],
            cc_name='supplychain_cc',
            wait_for_event=True   # Wait for event confirmation
        )
        return response
    except Exception as e:
        print(f"Error creating order {order_id}: {str(e)}")
        return None

# Get order details from the blockchain
def get_order(order_id):
    try:
        # Query the chaincode to get order details
        response = fabric_client.chaincode_query(
            requestor=admin_user,
            channel_name='supplychain-channel',
            peers=['peer0.org1.example.com'],
            args=[order_id],
            cc_name='supplychain_cc'
        )
        return json.loads(response)
    except Exception as e:
        print(f"Error retrieving order {order_id}: {str(e)}")
        return None

# Update order status
def update_order_status(order_id, status):
    try:
        # Invoke the chaincode to update the order status
        response = fabric_client.chaincode_invoke(
            requestor=admin_user,
            channel_name='supplychain-channel',
            peers=['peer0.org1.example.com'],
            args=[order_id, status],
            cc_name='supplychain_cc',
            wait_for_event=True   # Wait for event confirmation
        )
        return response
    except Exception as e:
        print(f"Error updating order {order_id}: {str(e)}")
        return None

# Load the CSV data
try:
    df = pd.read_csv('orders.csv')
except FileNotFoundError as e:
    print(f"Error loading CSV file: {str(e)}")
    df = None

if df is not None:
    # Iterate through the data and create orders on the blockchain
    for index, row in df.iterrows():
        order_id = str(row['orderId'])
        manufacturer_id = str(row['manufacturerId'])
        product_details = str(row['productDetails'])
        response = create_order(order_id, manufacturer_id, product_details)
        if response:
            print(f"Order {order_id} created successfully.")
        else:
            print(f"Failed to create order {order_id}.")
