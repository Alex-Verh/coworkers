from django.views.generic.edit import FormMixin
from .forms import ExperienceForm


class ExperienceFormMixin(FormMixin):
    form_class = ExperienceForm

    def get_form(self):
        return super().get_form()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experience_form'] = self.get_form()
        return context
