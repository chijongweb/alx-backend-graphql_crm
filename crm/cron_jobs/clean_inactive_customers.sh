#!/bin/bash

# Get current script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/../.." || exit 1  # Go to the root of the Django project

# Activate virtual environment if needed
# source venv/bin/activate

# Log file path
LOG_FILE="/tmp/customer_cleanup_log.txt"
DATE=$(date "+%Y-%m-%d %H:%M:%S")

# Run the cleanup inside Django shell and capture deleted count
DELETED_COUNT=$(python manage.py shell <<EOF
from crm.models import Customer
from datetime import datetime, timedelta
cutoff_date = datetime.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(last_order_date__lt=cutoff_date).delete()
print(deleted)
EOF
)

# Log result
if [ "$DELETED_COUNT" -gt 0 ]; then
    echo "$DATE - Deleted $DELETED_COUNT inactive customers." >> "$LOG_FILE"
else
    echo "$DATE - No inactive customers to delete." >> "$LOG_FILE"
fi