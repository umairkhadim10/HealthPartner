import django_tables2 as tables
from .models import *


class ItemsTable(tables.Table):
    class Meta:
        model = ItemSubmissionDate
        fields = ['create_date', 'calories']
