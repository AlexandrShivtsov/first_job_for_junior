import pytest
# from django.urls import reverse

URL = 'http://127.0.0.1:8000/accounts/auth/login/'


@pytest.mark.django_db
def test_login_form(client):
    responce = client.get(URL)
    assert responce.status_code == 200


@pytest.mark.django_db
def test_login_form_empti(client):
    responce = client.post(URL, data={})
    # if form is invalid, Django return status code 200
    assert responce.status_code == 200
    assert responce.context_data['form'].errors == {
        'username': ['This field is required.'],
        'password': ['This field is required.']
    }


@pytest.mark.django_db
def test_login_form_invalid(client, db):
    responce = client.post(URL, data={'username': '123', 'password': 'qwerty'})
    # if email address and password is invalid, Django return status code 200
    assert responce.status_code == 200
    assert responce.context_data['form'].error_messages == {
        'invalid_login': 'Please enter a correct %(username)s and password. '
        'Note that both fields may be case-sensitive.',
        'inactive': 'This account is inactive.'
    }
