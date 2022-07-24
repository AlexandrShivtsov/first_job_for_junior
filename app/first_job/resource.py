from import_export import resources
from first_job.models import Vacancy, ResponseLogs


class VacansyResource(resources.ModelResource):

    class Meta:
        model = Vacancy
        fields = (
            'title',
            'city',
            'employer',
            'salary',
            'description',
            'job_link',
            'created',
            'source',
        )


class ResponseLogsResource(resources.ModelResource):

    class Meta:
        model = ResponseLogs
        fields = (
            'created',
            'path',
            'status_code',
            'response_time',
        )
