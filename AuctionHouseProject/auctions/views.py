from django.shortcuts import render
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.urls import reverse,reverse_lazy

from django.http import Http404
from django.views import generic
from braces.views import SelectRelatedMixin
from . import models
from . import forms
from django.views.generic import TemplateView,CreateView
from django.contrib import messages

from django.contrib.auth import get_user_model
User=get_user_model()
# Create your views here.


class SignUp(CreateView):
    form_class=forms.UserCreateForm
    success_url = reverse_lazy('auction:login')
    template_name = 'auctions/signup.html'

# class Login()


