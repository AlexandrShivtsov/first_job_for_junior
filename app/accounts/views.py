from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, CreateView, RedirectView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from accounts.models import User

from accounts.forms import SingUpForm


# LoginRequiredMixin провеляет залогинен ли пользователь
class MyProfileView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    fields = (
        'first_name',
        'last_name',
        'phone',
        'email',
        'avatar',
    )
    success_url = reverse_lazy('index')
    template_name = 'my_profile.html'


    '''Ограничивает доступ пользователя только к своему профилю '''
    def get_object(self, queryset=None):
        return self.request.user


# class ChangePasswordView(LoginRequiredMixin, UpdateView):
#     queryset = User.objects.all()
#     fields = (
#         'password',
#     )
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         queryset = queryset.filter(id=self.request.user.id)
#         return queryset
#
#     success_url = reverse_lazy('my-profile')
#     template_name = 'change_password.html'

# class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
#     template_name = 'change_password.html'
#     success_message = "Successfully Changed Your Password"
#     success_url = reverse_lazy('my-profile')

class SingUpView(CreateView):
    model = User
    template_name = 'singe_up.html'
    success_url = reverse_lazy('index')
    form_class = SingUpForm


'''View для активации пользователя'''
class ActivateUserView(RedirectView):
    pattern_name = 'index'

    def get_redirect_url(self, *args, **kwargs):
        '''из url получаем username которого ранее определили в SingUpForm'''
        username = kwargs.pop('username')

        '''получаме user из db по извлеченному из url username если поле is_active=False'''
        user = get_object_or_404(User, username=username, is_active=False)

        '''изменяем user поле is_active с False на True'''
        user.is_active = True

        '''обновляет только одно поле "is_active"'''
        user.save(update_fields=('is_active',))

        return super().get_redirect_url(*args, **kwargs)
