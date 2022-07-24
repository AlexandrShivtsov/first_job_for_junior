import pytest


@pytest.mark.django_db
def test_index(client):
    responce = client.get('/')
    assert responce.status_code == 200
