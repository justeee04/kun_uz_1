from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from apps.news.models import Report


class ReportFilter(FilterSet):
    hash_tags = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Report
        fields = ('title', 'author', 'region_id', 'hash_tags')
