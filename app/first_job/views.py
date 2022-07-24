from urllib.parse import urlencode

from django.views.generic import TemplateView, ListView, DetailView, CreateView
from first_job.models import Vacancy, Articles, ContactUs
from first_job.forms import ContactUsForm
from django.urls import reverse_lazy
from django.core.cache import cache
from first_job.consts import CACHE_VACANSY_KEY
from django_filters.views import FilterView

from first_job.filters import VacancyFilter


class IndexView(TemplateView):
    template_name = 'index.html'


class VacancyView(FilterView):
    queryset = Vacancy.objects.all().order_by('-publication_date')
    template_name = 'vacancy.html'
    context_object_name = 'vacancy_list'
    paginate_by = 25
    filterset_class = VacancyFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        get_parameters = {}
        for key, value in self.request.GET.items():
            if key != 'page':
                get_parameters[key] = value
            context['paginations_params'] = urlencode(get_parameters)

        return context


# class VacancyView(TemplateView):
#     template_name = 'vacancy.html'
#     context_object_name = 'object'
#     paginate = 25
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         last_vacancy_upgrade = cache.get(CACHE_VACANSY_KEY)
#         if last_vacancy_upgrade is None:
#             last_vacancy_upgrade = Vacancy.objects.all().order_by('-publication_date')
#             cache.set(CACHE_VACANSY_KEY, last_vacancy_upgrade, 60 * 3)
#         context['vacancy_list'] = last_vacancy_upgrade
#         return context



class ArticlesView(ListView):
    queryset = Articles.objects.all().order_by('-created')
    template_name = 'articles.html'
    context_object_name = 'object'


class ArticlesDetailsView(DetailView):
    queryset = Articles.objects.all()
    template_name = 'full_text.html'


class ContactUsView(CreateView):
    model = ContactUs
    template_name = 'contact_us.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('index')


class VacancyDescriptionView(DetailView):
    queryset = Vacancy.objects.all()
    template_name = 'vacanсy_description.html'
    context_object_name = 'object'
