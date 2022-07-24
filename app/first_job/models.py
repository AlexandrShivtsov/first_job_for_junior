from django.db import models


class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    employer = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    description = models.CharField(max_length=4096)
    job_link = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=255)
    publication_date = models.DateField()

    class Meta:
        db_table = 'Вакансии'


class Articles(models.Model):
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=250)
    text = models.CharField(max_length=10240)
    author = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)


class ResponseLogs(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    status_code = models.PositiveSmallIntegerField()
    response_time = models.PositiveSmallIntegerField(help_text='in milliseconds')


class ContactUs(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=1000)
    from_email = models.EmailField()
