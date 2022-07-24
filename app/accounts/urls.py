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

from django.urls import path, include, reverse_lazy
from accounts.views import MyProfileView, SingUpView, ActivateUserView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
# from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [

    path('auth/', include('django.contrib.auth.urls')),
    path('my_profile/', MyProfileView.as_view(), name='my-profile'),

    path('change_password/',
         PasswordChangeView.as_view(
             template_name='change_password.html',
             success_url=reverse_lazy('accounts:password_change_done')),
         name='change-password'),

    path('change_password_done/',
         PasswordChangeDoneView.as_view(
             template_name='password_change_done.html'),
         name='password_change_done'),

    # TODO
    #
    # path('password_reset/',
    #      auth_views.PasswordResetView.as_view(
    #          template_name='password_reset_form.html'
    #      ),
    #      name='password_reset'),
    #
    # path('password_reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(
    #         template_name='password_reset_done.html'
    #      ),
    #      name='password_reset_done'),
    #
    # path('password_reset_confirm/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(
    #          template_name='password_reset_confirm.html'
    #      ),
    #      name='password_reset_confirm'),
    #
    # path('reset/done/',
    #      auth_views.PasswordResetCompleteView.as_view(
    #          template_name='password_reset_complete.html'
    #      ),
    #      name='password_reset_complete'),
    #
    # path('^', include('django.contrib.auth.urls')),

    path('sing_up/', SingUpView.as_view(), name='singe_up'),
    path('activate/<uuid:username>/', ActivateUserView.as_view(), name='activate_user'),
]
