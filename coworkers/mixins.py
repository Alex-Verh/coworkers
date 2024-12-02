from django.views.generic.edit import FormMixin, ContextMixin
from .forms import ExperienceForm, ContactForm


class ExperienceFormMixin(FormMixin):
    form_class = ExperienceForm

    def get_form(self):
        return super().get_form()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experience_form'] = self.get_form()
        return context


class ContactFormMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_form'] = ContactForm()
        return context
