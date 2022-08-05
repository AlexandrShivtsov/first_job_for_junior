from celery import shared_task
from django.core.mail import send_mail
from settings import settings


@shared_task
def activate_mail(activate_link, email_to):
    subject = 'Activate tour account today!',
    full_email_massage = f'''
           Hello!

           Here is your activation link {activate_link}
           '''

    send_mail(
        subject,
        full_email_massage,
        settings.EMAIL_HOST_USER,
        [email_to],
        fail_silently=False,
    )


@shared_task
def send_reset_password_link(reset_link, email_to):
    subject = 'Link for reset password',
    full_email_massage = f'''
           Hello!

           Here is your link for reset password {reset_link}
           '''

    send_mail(
        subject,
        full_email_massage,
        settings.EMAIL_HOST_USER,
        [email_to],
        fail_silently=False,
    )