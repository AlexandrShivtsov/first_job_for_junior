from rest_framework import generics
from first_job.models import Vacancy
from api.v1.serializers import VacancySerializer


'''ListCreateAPIView позоляет осуществлять как POST так и GET запросы'''


class VacancyApiView(generics.ListCreateAPIView):
    queryset = Vacancy.objects.all().order_by('-publication_date')
    serializer_class = VacancySerializer


'''RetrieveUpdateDestroyAPIView позволяет GET по конкретному обоъекту, PUT и DELETE '''


class VacancyDeleteUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacancy.objects.all().order_by('-publication_date')
    serializer_class = VacancySerializer


# '''ModelViewSet позволяет GET, CREATE, PUT и DELETE '''
# class VacancyApiViewSet(viewsets.ModelViewSet):
#     queryset = Vacancy.objects.all().order_by('-publication_date')
#     serializer_class = VacancySerializer
#     pagination_class = VacansyPagination
#     filterset_class = VacansyFilter
#     filter_backends = (
#         filters.DjangoFilterBackend,
#         rest_filters.OrderingFilter
#     )
#     ordering_fields = ['id']
#     throttle_classes = [AnnonUserVacancyTrottel]
