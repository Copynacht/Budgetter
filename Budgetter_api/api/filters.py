import django_filters
from .models import PaymentRecord

class PaymentRecordFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = PaymentRecord
        fields = ['category', 'payment', 'payment_detail', 'date', 'date_from', 'date_to']
