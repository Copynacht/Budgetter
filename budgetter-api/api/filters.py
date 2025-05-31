import django_filters
from .models import PaymentRecord

class PaymentRecordFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    month = django_filters.NumberFilter(field_name='date', lookup_expr='month')

    class Meta:
        model = PaymentRecord
        fields = ['payment', 'payment_detail', 'category', 'category_detail', 'date', 'date_from', 'date_to', 'year', 'month']
