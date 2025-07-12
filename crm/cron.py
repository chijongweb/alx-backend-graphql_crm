import datetime
import logging
import os
import requests

os.makedirs('/tmp', exist_ok=True)

log_file = '/tmp/crm_heartbeat_log.txt'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{timestamp} CRM is alive"
    try:
        response = requests.post('http://localhost:8000/graphql', json={'query': '{ hello }'})
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'hello' in data['data']:
                message += f" - GraphQL says: {data['data']['hello']}"
            else:
                message += " - GraphQL hello field missing"
        else:
            message += f" - GraphQL request failed with status {response.status_code}"
    except Exception as e:
        message += f" - GraphQL request error: {e}"
    with open(log_file, 'a') as f:
        f.write(message + '\n')
    print(message)
