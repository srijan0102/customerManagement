from django_filters import FilterSet, DateFilter, CharFilter
from .models import *

class OrderFilter(FilterSet):
    start_date = DateFilter(field_name='create_date', lookup_expr='gte')
    end_date = DateFilter(field_name='create_date', lookup_expr='lte')
    note = CharFilter(field_name='note', lookup_expr='icontains')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'create_date']
