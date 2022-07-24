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
from django.urls import path, include
from first_job.views import VacancyView, ArticlesView, ArticlesDetailsView, \
                            ContactUsView, VacancyDescriptionView

app_name = 'first_job'

urlpatterns = [
    path('vacancy/', VacancyView.as_view(), name='vacancy'),
    path('articles/', ArticlesView.as_view(), name='articles'),
    path('contact_us/', ContactUsView.as_view(), name='contact_us'),
    path('full_text/<int:pk>/', ArticlesDetailsView.as_view(), name='full_text'),
    path('vacancy_description/<int:pk>/', VacancyDescriptionView.as_view(), name='vacancy_description'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]
