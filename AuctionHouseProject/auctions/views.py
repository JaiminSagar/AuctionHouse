from django.shortcuts import render
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views import generic
from braces.views import SelectRelatedMixin
from . import models
from . import forms
from django.views.generic import TemplateView,CreateView,UpdateView,DetailView, ListView
from django.contrib import messages

from django.contrib.auth import get_user_model
User=get_user_model()
# Create your views here.


class SignUp(CreateView):
    form_class=forms.UserCreateForm
    success_url = reverse_lazy('auctions:login')
    template_name = 'auctions/signup.html'
#
class ProfileSetup(LoginRequiredMixin,CreateView):
    form_class = forms.ProfileSetupForm
    success_url = reverse_lazy('home')
    template_name = 'auctions/profile_form.html'

class ProfileUpdate(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'auctions/profile_detail.html'
    template_name_suffix = '_profile_form'
    form_class = forms.ProfileSetupForm
    model = models.User

class ProfileDetail(LoginRequiredMixin,DetailView):
    model = models.User

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class BecomeAgent(CreateView):
    form_class = forms.BecomeAgentForm
    success_url = reverse_lazy('home')
    template_name = 'auctions/become_agent.html'

class Thanks(TemplateView):
    template_name = 'auctions/thanks.html'


class AuctionList(ListView, LoginRequiredMixin):
    model = models.CurrentAuction
    template_name = 'auctions/auction_list.html'

# class Welcome(TemplateView):
#

# class Login()

