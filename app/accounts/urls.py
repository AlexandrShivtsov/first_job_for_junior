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
from accounts.views import MyProfileView, SingUpView, ActivateUserView, \
    ResetPasswordView, CheckResetPasswordLinkView, WrongInputEmailResetPasswordView, \
    ResetPasswordInputView, PasswordDoNotMatchView, InfoMessageResetPasswordView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

app_name = 'accounts'

urlpatterns = [

    path('auth/', include('django.contrib.auth.urls')),
    path('my_profile/', MyProfileView.as_view(), name='my-profile'),

    path('change_password/', PasswordChangeView.as_view(
        template_name='change_password.html',
        success_url=reverse_lazy('accounts:password_change_done')),
        name='change-password'),

    path('change_password_done/', PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'),
        name='password_change_done'),

    path('reset_password_custom/', ResetPasswordView.as_view(),
         name='reset_password_custom'),

    path('reset_password_sent_custom/<uuid:username>/', CheckResetPasswordLinkView.as_view(),
         name='reset_password_sent_custom'),

    path('wrong_input_email/', WrongInputEmailResetPasswordView.as_view(),
         name='wrong_input_email'),

    path('reset_password_input/<uuid:username>', ResetPasswordInputView.as_view(),
         name='reset_password_input'),

    path('sing_up/', SingUpView.as_view(),
         name='singe_up'),

    path('activate/<uuid:username>/', ActivateUserView.as_view(),
         name='activate_user'),

    path('password_do_not_match/', PasswordDoNotMatchView.as_view(),
         name='password_do_not_match'),

    path('info_message_about_send_link/', InfoMessageResetPasswordView.as_view(),
         name='info_message_about_send_link'),
]
