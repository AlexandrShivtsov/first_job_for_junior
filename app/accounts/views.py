from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, CreateView, RedirectView, TemplateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.urls import reverse
from accounts.models import User
from accounts.tasks import send_reset_password_link
from django.conf import settings
from django.http import HttpResponseRedirect
from accounts.forms import SingUpForm, ResetPasswordForm, ResetPasswordInputForm


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


class ResetPasswordView(FormView):
    template_name = 'reset_password/reset_password.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('accounts:info_message_about_send_link')

    def form_valid(self, form):
        '''Проверяем валидна ли форма'''

        user_email = form.data['email']
        '''Извлекаем из форми информацию о email позлователя'''
        try:
            user_object = User.objects.get(email=user_email)
            '''Получаем объкт позлователя из базы данных'''

        except User.DoesNotExist:
            return HttpResponseRedirect(reverse('accounts:wrong_input_email'))
        '''если пользователя с указанным email не существует перенаправляем на страницу с ошибкой'''

        '''составили ссылку для активации'''
        reset_password_link = reverse("accounts:reset_password_sent_custom", args=[user_object.username])

        '''отправили ссылку для активации'''
        send_reset_password_link.delay(
            f'{settings.HTTP_SHCEMA}://{settings.DOMAIN}{reset_password_link}',
            user_object.email
        )

        return super().form_valid(form)


class CheckResetPasswordLinkView(RedirectView):
    pattern_name = 'accounts:reset_password_input'
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        '''из url получаем username которого указали в ссылке на восттановление пароля'''

        username = kwargs.get('username')

        user = get_object_or_404(User, username=username)
        '''Получаем объект пользователя из базы данных'''

        if str(username) == user.username:
            '''Сравниваем совпадают ли имя пользователя из url и то которое получили из базы данных,
            если они совподають перенаправляем на страницу обновления пароля'''

            return super().get_redirect_url(*args, **kwargs)


class WrongInputEmailResetPasswordView(TemplateView):
    template_name = 'reset_password/wrong_input_email.html'


class ResetPasswordInputView(FormView):
    template_name = 'reset_password/reset_password_input.html'
    form_class = ResetPasswordInputForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        if form.data['new_password'] != form.data['chek_password']:
            '''Проверяем совпадают ли введенные пароли, если нет, перенаправляем на страницу с ошибкой'''
            return HttpResponseRedirect(reverse('accounts:password_do_not_match'))

        url_path = self.request.path_info
        '''Получаем url'''

        username = url_path.split('/')[-1]
        '''Извлекаем username'''

        user_object = User.objects.get(username=username)
        '''Получаем объект пользователя'''
        print(user_object.password)

        new_password = form.data['chek_password']

        user_object.set_password(new_password)
        user_object.save()
        '''Сохраняем новый пароль'''

        return super(ResetPasswordInputView, self).form_valid(form)

class PasswordDoNotMatchView(TemplateView):
    template_name = 'reset_password/password_do_not_match.html'


class InfoMessageResetPasswordView(TemplateView):
    template_name = 'reset_password/info_message_about_send_link.html'






















































    # success_url = reverse_lazy('index')
    #
    # def get(self, request, *args, **kwargs):
    #     form = ResetPasswordForm()
    #     return render(request, self.template_name, {'form': form})
    #
    # def post(self, request, *args, **kwargs):
    #     form = ResetPasswordForm()
    #     if form.is_valid():
    #         text = form.clean_data['email']
    #         print(text)
    #     return render(request, self.template_name, {'form': form})
    #
    #
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if 'POST' in self.request.method:
    #         context['email'] = context['form'].data['email']
    #         breakpoint()
    #         print(context['email'])
    #     return context
    #
    #
    #
