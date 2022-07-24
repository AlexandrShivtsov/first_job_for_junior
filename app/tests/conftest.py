import pytest
# from django.core.management import call_command
from rest_framework.test import APIClient
# from accounts.models import User


# @pytest.fixture(autouse=True, scope='function')
# def enable_db_for_all_tests(db):

#
# @pytest.fixture(autouse=True, scope='session')
# def load_fixtures(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         breakpoint()
#         call_command('loaddata', 'tests/fixtures/vacancy.json')

@pytest.fixture(autouse=True, scope='function')
def api_client_auth(django_user_model):
    api_client = APIClient()

    password = 'password'
    user = django_user_model(
        email='example@example.com'
    )
    user.set_password(password)
    user.save()
    api_token = api_client.post('/api/v1/token/', data={'email': user.email, 'password': user.password},)
    breakpoint()
    assert api_token.status_code == 200
