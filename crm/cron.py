import datetime
import os
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    log_file = '/tmp/crm_heartbeat_log.txt'
    timestamp = datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)
        
        query = gql("""
        query {
            hello
        }
        """)
        result = client.execute(query)
        message = f"{timestamp} CRM is alive. GraphQL says: {result['hello']}\n"
    except Exception as e:
        message = f"{timestamp} CRM heartbeat failed: {e}\n"

    with open(log_file, "a") as f:
        f.write(message)

def update_low_stock():
    log_file = '/tmp/low_stock_updates_log.txt'
    timestamp = datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S')

    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)

        mutation = gql("""
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    name
                    stock
                }
                message
            }
        }
        """)

        result = client.execute(mutation)
        updated_products = result["updateLowStockProducts"]["updatedProducts"]
        message = result["updateLowStockProducts"]["message"]

        log_lines = [f"{timestamp} {message}\n"]
        for p in updated_products:
            log_lines.append(f" - {p['name']} stock updated to {p['stock']}\n")

    except Exception as e:
        log_lines = [f"{timestamp} Failed to update low-stock products: {e}\n"]

    with open(log_file, "a") as f:
        f.writelines(log_lines)