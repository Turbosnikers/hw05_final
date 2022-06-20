from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm, ContactForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class Contact(CreateView):
    form_class = ContactForm
    template_name = 'users/contact.html'
