#!/bin/bash

deleted_count=$(python manage.py shell -c "
from django.utils.timezone import now
from datetime import timedelta
from crm.models import Customer, Order

cutoff_date = now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(order__order_date__lt=cutoff_date).distinct()
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt
