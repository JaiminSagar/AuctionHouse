from django.shortcuts import render
from django.contrib.auth.mixins import  LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views import generic
from braces.views import SelectRelatedMixin
from . import models
from . import forms
from django.contrib.auth import views as auth_view,login
from django.views.generic import TemplateView,CreateView,UpdateView,DetailView
from django.contrib import messages
from django.http import HttpResponse

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
    template_name= 'user_profile_form'
    form_class = forms.ProfileSetupForm
    model = models.User

class ProfileDetail(LoginRequiredMixin,SelectRelatedMixin,DetailView):
    template_name = 'profile_detail'
    model = models.User
    select_related = ('first_name','last_name','mobile','email','address','image','city','state','pincode')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class BecomeAgent(CreateView):
    form_class = forms.BecomeAgentForm
    success_url = reverse_lazy('home')
    template_name = 'auctions/become_agent.html'

class Thanks(TemplateView):
    template_name = 'auctions/thanks.html'


@login_required
def profile_setup(request):
    form_class=forms.ProfileSetupForm

    if request.method == "POST":
        print(request.POST)
        user_form= form_class(data=request.POST)
        # image =request.POST['image']
        print(user_form.username)
        if user_form.is_valid():
            user = user_form.save()
            user.save()
            return HttpResponse("<h1>You will be redirected to profile page.</h1>")
        else:
            print("Not Done")
            return HttpResponse("Not Done Yet.</h1>")


