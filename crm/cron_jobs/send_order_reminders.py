#!/usr/bin/env python3

import requests
import datetime
import logging

# Set up logging
log_file = "/tmp/order_reminders_log.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Calculate date one week ago
one_week_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")

# Define GraphQL query
query = """
query GetRecentOrders {
  orders(orderDate_Gte: "%s") {
    id
    customer {
      email
    }
  }
}
""" % one_week_ago

# Send request to GraphQL endpoint
response = requests.post(
    "http://localhost:8000/graphql",
    json={"query": query}
)

if response.status_code == 200:
    data = response.json().get("data", {})
    orders = data.get("orders", [])

    if orders:
        for order in orders:
            order_id = order["id"]
            email = order["customer"]["email"]
            logging.info(f"Order ID: {order_id}, Customer Email: {email}")
    else:
        logging.info("No recent orders found.")
    print("Order reminders processed!")
else:
    logging.error(f"Failed to fetch data from GraphQL. Status code: {response.status_code}")
    print("Failed to fetch data from GraphQL.")
