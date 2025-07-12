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