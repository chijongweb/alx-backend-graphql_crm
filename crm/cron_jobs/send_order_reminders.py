#!/usr/bin/env python3
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import datetime
import logging
import os

# Ensure /tmp directory exists
os.makedirs('/tmp', exist_ok=True)
log_file = '/tmp/order_reminders_log.txt'

logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Define date 7 days ago
seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')

# Set up GraphQL transport
transport = RequestsHTTPTransport(
    url='http://localhost:8000/graphql',
    verify=False,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=False)

# Define the GraphQL query
query = gql("""
query {
  orders(orderDate_Gte: "%s") {
    id
    customer {
      email
    }
  }
}
""" % seven_days_ago)

try:
    result = client.execute(query)
    orders = result.get("orders", [])

    for order in orders:
        order_id = order["id"]
        email = order["customer"]["email"]
        logging.info(f"Reminder for Order ID {order_id} to {email}")

    print("Order reminders processed!")

except Exception as e:
    logging.error(f"Failed to fetch or log orders: {e}")
    print("An error occurred while processing reminders.")