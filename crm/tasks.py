from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=True, retries=3)
    client = Client(transport=transport, fetch_schema_from_transport=False)

    query = gql("""
    query {
        allCustomers { id }
        allOrders { id totalAmount }
    }
    """)
    
    try:
        result = client.execute(query)
        total_customers = len(result['allCustomers'])
        total_orders = len(result['allOrders'])
        total_revenue = sum(float(order['totalAmount']) for order in result['allOrders'])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"

        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(report)
    except Exception as e:
        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(f"Report generation failed: {str(e)}\n")
