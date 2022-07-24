from django_filters import rest_framework as filters

from first_job.models import Vacancy


class VacansyFilter(filters.FilterSet):

    class Meta:

        model = Vacancy
        fields = {
            'created': ('gte', 'lte'),
        }
