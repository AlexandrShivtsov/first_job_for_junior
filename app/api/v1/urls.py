"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
# from app.api.views import VacancyApiView, VacancyDeleteUpdateApiView, VacancyApiViewSet
from api.v1.views import VacancyApiView, VacancyDeleteUpdateApiView
# from api.v1.views import VacancyApiViewSet
# from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)

app_name = 'api'

# router = DefaultRouter()
# router.register(r'vacancy', VacancyApiViewSet, basename='vacancy')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path('vacancy/', VacancyApiView.as_view()),
    path('vacancy/<int:pk>/', VacancyDeleteUpdateApiView.as_view()),

]

# urlpatterns = [router.urls]
