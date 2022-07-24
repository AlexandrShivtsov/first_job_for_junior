import django_filters
from first_job.models import Vacancy
from django.forms import DateInput


class VacancyFilter(django_filters.FilterSet):

    publication_date_gte = django_filters.DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        field_name='publication_date',
        lookup_expr='gte',
        label='Дата публикации c'
    )

    publication_date_lte = django_filters.DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        field_name='publication_date',
        lookup_expr='lte',
        label='Дата публикации по'
    )

