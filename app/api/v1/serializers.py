from rest_framework import serializers
from first_job.models import Vacancy


class VacancySerializer(serializers.ModelSerializer):

    class Meta:
        model = Vacancy
        fields = (
            'id',
            'title',
            'city',
            'employer',
            'salary',
            'job_link',
            'source',
            'publication_date',
        )
