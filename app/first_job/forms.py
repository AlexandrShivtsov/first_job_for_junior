from django import forms
from first_job.models import ContactUs
from first_job.tasks import contact_us_mail


class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = (
            'subject',
            'message',
            'from_email',
        )

    def clean(self):
        '''получем данные из формы и отправляем email через tasks:activate_mail'''
        cleaned_data = super().clean()
        contact_us_mail.delay(email_to=cleaned_data['from_email'])
        return cleaned_data
