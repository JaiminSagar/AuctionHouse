from django.shortcuts import render, redirect
from django.contrib.auth.mixins import  LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import Http404,HttpResponseRedirect
from django.views import generic
from braces.views import SelectRelatedMixin
from . import models
from . import forms
from django.contrib.auth import views as auth_view,login
from django.views.generic import TemplateView,CreateView,UpdateView,DetailView, ListView
from django.contrib import messages
from django.http import HttpResponse

from django.contrib.auth import get_user_model
User=get_user_model()

# email and activation related libraries
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User as Signup_User
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


# class SignUp(CreateView):
#     form_class=forms.UserCreateForm
#     success_url = reverse_lazy('auctions:login')
#     template_name = 'auctions/signup.html'

def signup(request):
    if request.method == 'POST':
        form = forms.UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'AuctionHouse.in | Activate Your Account '
            message = render_to_string('auctions/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = forms.UserCreateForm()
    return render(request, 'auctions/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Signup_User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('profile_check')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

class ProfileUpdate(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    # redirect_field_name = 'auctions/profile_detail.html'
    template_name= 'auctions/user_profile_form.html'
    form_class = forms.ProfileUpdateForm
    model = models.UserDetails

class ProfileDetail(LoginRequiredMixin,SelectRelatedMixin,DetailView):
    template_name = 'auctions/profile_detail.html'
    model = models.UserDetails
    select_related = ('user',)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))


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

class ProfileSetup(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = models.UserDetails
    template_name = 'auctions/user_profile_form.html'
    # redirect_field_name = 'auctions/profile_detail.html'
    form_class = forms.ProfileSetupForm

    def form_valid(self, form):
        # print(self.request.user)
        profile =form.save(commit=False)
        profile.user=models.User.objects.get(username=self.request.user)
        profile.user.profile_set()
        profile.save()
        return super().form_valid(form)

