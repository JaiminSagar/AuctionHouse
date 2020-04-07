from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.mixins import  LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import Http404,HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import FormView
from braces.views import SelectRelatedMixin
from . import models
from . import forms
from django.contrib.auth import views as auth_view,login
from django.views.generic import TemplateView,CreateView,UpdateView,DetailView, ListView,View
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
            return render(request,'auctions/email_confirm.html',{'msg':"Please confirm your email address to complete the registration."})
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
        return queryset.filter(city__city_name__iexact=agent.city)


class PropertyDetailsForAgent(LoginRequiredMixin, DetailView):
    model = models.PropertyReg
    template_name = 'auctions/agent/property_details_agent.html'
    # form_class = forms.PropertyDescriptionForm


    def get_context_data(self, **kwargs):
        context =super().get_context_data()
        # context['form']=self.form_class
        # context['detail_pk']=self.pk

        if not models.PropertyFilesUpload.objects.all().filter(property_reg__id=self.kwargs.get('pk')):
            context['file_list'] = []
        else:    
            context['file_list'] = models.PropertyFilesUpload.objects.all().filter(property_reg__id=self.kwargs.get('pk'))


        if not models.PropertyImagesUpload.objects.all().filter(property_reg__id=self.kwargs.get('pk')):
            context['image_list'] =[]    
        else:
            context['image_list'] = models.PropertyImagesUpload.objects.all().filter(property_reg__id=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))


    def post(self,*args,**kwargs):
        form = forms.PropertyDescriptionForm(self.request.POST)
        if form.is_valid():
            prop = get_object_or_404(models.PropertyReg,pk=self.kwargs.get('pk'))
            agent = get_object_or_404(models.AgentUser, pk=self.request.user.pk)
            prop.property_description=form.cleaned_data['property_description']
            prop.agent_id = agent
            prop.save()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return HttpResponseRedirect("<h1>try again</h1>")

        # def form_valid(self, form):
        #     # print(self.request.user)
        #     # request=self.request
        #     # image= request.FILES['field_name']
        #     # form.iamge =image
        #     print("hi")
        #     prop = form.save(commit=False)
        #     agent = get_object_or_404(models.AgentUser, pk=self.request.user.pk)
        #     prop.agent_id = agent
        #     prop.save()
        #     return super().form_valid(form)

    # def form_valid(self, form):
    #     # print(self.request.user)
    #     # request=self.request
    #     # image= request.FILES['field_name']
    #     # form.iamge =image
    #     prop = form.save(commit=False)
    #     print(prop.pk)
    #     agent = get_object_or_404(models.AgentUser, pk=self.request.user.pk)
    #     prop.agent_id = agent 
    #     prop.save()
    #     #return super().form_valid(form)


def submit_property(request, pk):
    prop = get_object_or_404(models.PropertyReg, pk=pk)
    agent = get_object_or_404(models.AgentUser, pk=request.user.pk)
    prop.submit()
    prop.agent_id = agent
    prop.save()
    return redirect('auctions:agent_property_details', pk=pk)


def add_property_description(request, pk):
    if request.method == 'POST':
        form = forms.PropertyDescriptionForm(request.POST)
        if form.is_valid():
            prop = get_object_or_404(models.PropertyReg,pk=pk)
            # agent = get_object_or_404(models.AgentUser, pk=request.user.pk)
            prop.property_description=form.cleaned_data['property_description']
            prop.pre_set_amount = int(form.cleaned_data['pre_set_amount'])
            # prop.agent_id = agent
            prop.save()
            return redirect('auctions:agent_property_details', pk=prop.pk)
    else:
        form = forms.PropertyDescriptionForm()
    return render(request, 'auctions/agent/add_property_description.html', {'form': form})


# class PropertyFilesUploadView(FormView):
#     form_class = forms.PropertyFilesUploadForm
#     template_name = 'auctions/agent/add_property_files.html'  # Replace with your template.
#     # success_url = reverse_lazy('auctions:add_files', kwargs={'pk': })  # Replace with your URL or reverse().

#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('document')
#         prop = get_object_or_404(models.PropertyReg, pk=self.kwargs.get('pk'))
#         if form.is_valid():
#             for f in files:
#                 doc = models.PropertyFilesUpload(property_reg=prop, document=f)
#                 print(doc)
#                 doc.save()
#             # return redirect('auctions:add_files', pk=self.kwargs.get('pk'))
#             return redirect('auctions:agent_property_details', pk=self.kwargs.get('pk'))

def propertyFilesUploadView(request, pk):
    if request.method == 'POST':
        print("post")
        form = forms.PropertyFilesUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print("valid")
            prop = get_object_or_404(models.PropertyReg, pk=pk)
            print(prop)
            for f in request.FILES.getlist('document'):
                models.PropertyFilesUpload.objects.create(property_reg=prop, document=f)
            return redirect('auctions:agent_property_details', pk=pk)
    else:
        form = forms.PropertyFilesUploadForm()
    return render(request, 'auctions/agent/add_property_files.html', {'form': form})


def propertyImagesUploadView(request, pk):
    if request.method == 'POST':
        print("post")
        form = forms.PropertyImagesUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print("valid")
            prop = get_object_or_404(models.PropertyReg, pk=pk)
            print(prop)
            for f in request.FILES.getlist('image'):
                models.PropertyImagesUpload.objects.create(property_reg=prop, image=f)
            return redirect('auctions:agent_property_details', pk=pk)
    else:
        form = forms.PropertyImagesUploadForm()
    return render(request, 'auctions/agent/add_property_images.html', {'form': form})
                

# class PropertyImagesUploadView(FormView):
#     form_class = forms.PropertyImagesUploadForm
#     template_name = 'auctions/agent/add_property_images.html'  # Replace with your template.
#     # success_url = '...'  # Replace with your URL or reverse().

#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('image')
#         prop = get_object_or_404(models.PropertyReg, pk=self.kwargs.get('pk'))
#         if form.is_valid():
#             for f in files:
#                 img = models.PropertyImagesUpload(property_reg=prop, document=f)
#                 img.save()
#             #return redirect('auctions:add_images', pk=self.kwargs.get('pk'))
#             return redirect('auctions:agent_property_details', pk=self.kwargs.get('pk'))



class PropertyDetailsForUser(LoginRequiredMixin, DetailView):
    model = models.PropertyReg
    template_name = 'auctions/user/property_details_user.html'
    
    def get_context_data(self, **kwargs):
        context =super().get_context_data()

        if not models.PropertyFilesUpload.objects.all().filter(property_reg__id=self.kwargs.get('pk')):
            context['file_list'] = []
        else:    
            context['file_list'] = models.PropertyFilesUpload.objects.all().filter(property_reg__id=self.kwargs.get('pk'))


        if not models.PropertyImagesUpload.objects.all().filter(property_reg__id=self.kwargs.get('pk')):
            context['image_list'] =[]    
        else:
            context['image_list'] = models.PropertyImagesUpload.objects.all().filter(property_reg__id=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))

        


# class PropertyDescriptionSetup(LoginRequiredMixin, UpdateView):
#     model = models.PropertyReg
#     template_name = 'auctions/agent/property_details_agent.html'
#     form_class = forms.PropertyDescriptionForm

#     def form_valid(self, form):
#         # print(self.request.user)
#         prop =form.save(commit=False)
#         agent = get_object_or_404(models.AgentUser, pk=self.request.user.pk)
#         prop.agent_id = agent 
#         prop.save()
#         return super().form_valid(form)

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

class CurrentAuctionList(ListView):
    model = models.CurrentAuction
    template_name = "auctions/auction_list.html"

    def get(self, request, *args, **kwargs):
        current_auction_all=models.CurrentAuction.objects.all().filter(current_auction_status=False)
        for auction in current_auction_all:
            # if auction.auction_start_date == t
            pass
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(current_auction_status=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        context['image_list'] = models.PropertyImagesUpload.objects.all()
        return context

class CurrentAuctionDetails(DetailView):
    model = models.CurrentAuction
    template_name = "auctions/auction_details.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form']=forms.MakeAnOffer
        auction_bid=models.BiddingOfProperty.objects.all().filter(current_auction_id=self.kwargs.get('pk')).order_by('-user_bid_amount')
        context['past_bids']=auction_bid
        return context

class AuctionBid(LoginRequiredMixin,View):
    login_url = '/login/'

    def post(self,*args,**kwargs):
        current_auction_data =get_object_or_404(models.CurrentAuction,pk=self.kwargs.get('pk'))
        user = get_object_or_404(models.User, pk=int(self.request.POST['user']))
        register= models.RegForAuction.objects.all().filter(current_auction_id=self.kwargs.get('pk'))
        for entry in register:
            if entry.user_id == user.pk:
                if current_auction_data.next_bid <= float(self.request.POST['user_bid']):
                    bid_of_user = models.BiddingOfProperty.objects.create(current_auction_id=current_auction_data,user=user)
                    bid_of_user.user_bid_amount = float(self.request.POST['user_bid'])
                    current_auction_data.current_amount = float(self.request.POST['user_bid'])
                    current_auction_data.highest_bidder=user
                    current_auction_data.bidding()
                    current_auction_data.save()
                    bid_of_user.save()
                    return HttpResponseRedirect(
                        reverse_lazy('auctions:auction_detail', kwargs={'pk': current_auction_data.pk}))
                else:
                    messages.error(self.request, "Please Enter the correct amount based on increment ratio.")
                    return HttpResponseRedirect(reverse_lazy('auctions:auction_detail', kwargs={'pk': current_auction_data.pk}))
            else:
                messages.error(self.request, "You have to register for participating in auction. Click on the Register for participating.")
                return HttpResponseRedirect(reverse_lazy('auctions:auction_detail', kwargs={'pk': current_auction_data.pk}))

        messages.error(self.request,"You have to register for participating in auction. Click on the Register for participating.")
        return HttpResponseRedirect(reverse_lazy('auctions:auction_detail', kwargs={'pk': current_auction_data.pk}))

class UpcommingAuctionList(ListView):
    model = models.CurrentAuction
    template_name = "auctions/up_comming_auction_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(current_auction_status=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        context['image_list'] = models.PropertyImagesUpload.objects.all()
        return context