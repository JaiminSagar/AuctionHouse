from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import  LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
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


class ApplyEvaluation(LoginRequiredMixin, CreateView):
    model = models.PropertyReg
    template_name = 'auctions/user/evaluation.html'
    #redirect_field_name = 'auctions/user/evaluation_list.html'
    success_url = reverse_lazy('auctions:user_evaluation_list')
    form_class = forms.ApplyEvaluationForm

    def form_valid(self, form):
        prop = form.save(commit = False)
        prop.user = models.User.objects.get(username=self.request.user)
        prop.save()
        return super().form_valid(form)
    

class UserEvalutionList(LoginRequiredMixin,ListView):
    model = models.PropertyReg
    template_name = 'auctions/user/user_evaluation_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.request.user.username)

class EvaluationListForAgent(LoginRequiredMixin, ListView):
    model = models.PropertyReg
    template_name = 'auctions/agent/agent_dashboard.html'
    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        agent = get_object_or_404(models.AgentUser, pk=self.request.user.pk)
        print(agent.city)
        return queryset.filter(city__iexact=agent.city)


class ProfileUpdate(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    # redirect_field_name = 'auctions/profile_detail.html'
    template_name= 'auctions/user/user_profile_form.html'
    form_class = forms.ProfileUpdateForm
    model = models.UserDetails

class ProfileDetail(LoginRequiredMixin,SelectRelatedMixin,DetailView):
    template_name = 'auctions/user/profile_detail.html'
    model = models.UserDetails
    select_related = ('user',)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))

class AgentDetailView(LoginRequiredMixin,SelectRelatedMixin,DetailView):
    template_name = 'auctions/agent/agent_details.html'
    model = models.AgentUser
    select_related = ('user_ptr',)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))

class AgentUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    # redirect_field_name = 'auctions/profile_detail.html'
    template_name = 'auctions/agent/agent_profile_form.html'
    form_class = forms.AgentProfileForm
    model = models.AgentUser

class BecomeAgent(CreateView):
    form_class = forms.BecomeAgentForm
    success_url = reverse_lazy('home')
    template_name = 'auctions/agent/become_agent.html'

    def form_valid(self, form):
        agent = form.save(commit = False)
        agent.is_staff=True
        agent.username = agent.email
        agent.save()
        mail_subject = 'AuctionHouse.in | Successfully Appiled '
        message = render_to_string('auctions/becomeAgent_email.html', {
            'agent': agent,
        })
        to_email = agent.email
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        return super().form_valid(form)

class Thanks(TemplateView):
    template_name = 'auctions/thanks.html'


class AuctionList(ListView, LoginRequiredMixin):
    model = models.CurrentAuction
    template_name = 'auctions/auction_list.html'


class ProfileSetup(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = models.UserDetails
    template_name = 'auctions/user/user_profile_form.html'
    # redirect_field_name = 'auctions/profile_detail.html'
    form_class = forms.ProfileSetupForm

    def form_valid(self, form):
        # print(self.request.user)
        profile =form.save(commit=False)
        profile.user=models.User.objects.get(username=self.request.user)
        profile.user.profile_set()
        profile.save()
        return super().form_valid(form)


def set_agent_password(request, pk):
    agent = get_object_or_404(models.AgentUser, pk=pk)
    
    if agent.password == '':
        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm password')
            print(password, confirm_password)
            print(make_password(password), make_password(confirm_password))

            if password == confirm_password:
                agent.password = make_password(password)
                agent.save()
                return HttpResponse('Your password sucessfully saved. Now do Login.')
        return render(request, 'auctions/set_agent_password.html', {})

    return HttpResponse("Maybe Your password is already there.....")

