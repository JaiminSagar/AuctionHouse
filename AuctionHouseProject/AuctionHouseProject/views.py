from django.shortcuts import render
from django.views.generic import TemplateView,CreateView
from auctions.models import User,UserDetails
from auctions import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import settings,get_user
from django.contrib import messages
from django.contrib.auth import get_user_model
# Create your views here.
#
user=get_user_model()

def checking(request):
    if request.user:
        user=get_user(request)
        if user.user.profile_setup == False:
            return HttpResponseRedirect(reverse('auctions:setup_profile'))
        else:
            return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('home'))


class HomePage(TemplateView):
    template_name = 'index.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

