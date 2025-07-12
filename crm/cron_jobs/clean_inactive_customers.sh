#!/bin/bash

# Save current working directory for logging/debugging
cwd=$(pwd)

# Navigate to the root of the Django project
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/../.." || exit 1

# Log file
LOG_FILE="/tmp/customer_cleanup_log.txt"
DATE=$(date "+%Y-%m-%d %H:%M:%S")

# Run Django shell to delete inactive customers
DELETED_COUNT=$(python manage.py shell <<EOF
from crm.models import Customer
from datetime import datetime, timedelta
cutoff = datetime.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(last_order_date__lt=cutoff).delete()
print(deleted)
EOF
)

# Log result with cwd
if [ "$DELETED_COUNT" -gt 0 ]; then
    echo "$DATE - Deleted $DELETED_COUNT inactive customers. (cwd: $cwd)" >> "$LOG_FILE"
else
    echo "$DATE - No inactive customers to delete. (cwd: $cwd)" >> "$LOG_FILE"
fi