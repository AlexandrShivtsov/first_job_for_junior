import pytest
# from django.urls import reverse

from first_job.models import ContactUs

URL = 'http://127.0.0.1:8000/first_job/contact_us/'


@pytest.mark.django_db
def test_contact_us_form(client, db):

    responce = client.get(URL)
    assert responce.status_code == 200


# @pytest.mark.django_db
def test_contact_us_valid_data(client, db, mailoutbox):

    numbers_records_in_contact_us = ContactUs.objects.count()
    responce = client.post(URL, data={'subject': 'test', 'message': 'test', 'from_email': 'test@test.com'})
    # if form is valid, Django return status code 302 and redirect to '/'
    assert responce.status_code == 302
    assert responce.url == '/'
    assert ContactUs.objects.count() == numbers_records_in_contact_us + 1
