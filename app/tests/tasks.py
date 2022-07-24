from first_job.tasks import pars_work_ua
from unittest.mock import MagicMock


def test_pars_rabota_ua(db, mocker):
    requests_get_mock = mocker.patch('requests.get')
    requests_get_mock.return_value = MagicMock(text='MagicMock')
    pars_work_ua()
