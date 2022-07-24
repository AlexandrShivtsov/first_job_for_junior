from django.contrib import admin
from first_job.models import Articles, Vacancy, ResponseLogs
from rangefilter.filters import DateRangeFilter
from import_export.admin import ImportExportModelAdmin
from first_job.resource import VacansyResource, ResponseLogsResource


class ArticlesAdmin(admin.ModelAdmin):
    """Виводить у адміністративну панель модель Articles"""

    list_display = (
        'title',
        'short_description',
        'author',
        'created',

    )
    """Фільтрація статей за датою створення"""
    list_filter = (
        ('created', DateRangeFilter),
    )

    """Забороняе видалення статей"""
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Articles, ArticlesAdmin)


class VacancyAdmin(ImportExportModelAdmin):
    """Виводить у адміністративну панель модель Articles"""

    resource_class = VacansyResource

    list_display = (
        'title',
        'city',
        'employer',
        'salary',
        # 'description',
        'job_link',
        'created',
        'source',
        'publication_date',
    )

    """Фільтрація статей за датою створення та ресурсом на якому розміщено вакансію"""
    list_filter = (
        ('created', DateRangeFilter),
        'source',
    )

    """Пошук вкансый за полями 'title' та 'created'"""
    search_fields = (
        'title',
        'created',
    )

    """Поля 'source' та 'job_link' лише для читання"""
    readonly_fields = (
        'source',
        'job_link',
    )


admin.site.register(Vacancy, VacancyAdmin)


class ResponseLogsAdmin(ImportExportModelAdmin):
    """Виводить у адміністративну панель модель ResponseLogs"""

    resource_class = ResponseLogsResource

    list_display = (
        'created',
        'path',
        'status_code',
        'response_time',
    )


admin.site.register(ResponseLogs, ResponseLogsAdmin)
