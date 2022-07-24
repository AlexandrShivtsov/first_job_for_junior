from rest_framework.throttling import AnonRateThrottle


class AnnonUserVacancyTrottel(AnonRateThrottle):
    scope = 'vacancy_annon_trottle'
