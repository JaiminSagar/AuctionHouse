from django.shortcuts import render
from django.views.generic import TemplateView,CreateView
from auctions.models import User
from auctions import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import settings
from django.contrib import messages
# Create your views here.
#
class HomePage(TemplateView):
    template_name = 'index.html'
    # form_class = forms.ProfileSetupForm
    # success_url = reverse_lazy('auctions:profile_update')
    # template_name = 'index.html'
    users =User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = self.users
        # context['form']=forms.ProfileSetupForm()
        return context


class ThanksPage(TemplateView):
    template_name = 'thanks.html'

