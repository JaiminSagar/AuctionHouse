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
import math
from django.contrib.auth import views as auth_view,login
from django.views.generic import TemplateView,CreateView,UpdateView,DetailView, ListView,View
from django.contrib import messages
from django.http import HttpResponse
import datetime
from django.utils import timezone
from . filters import AuctionFilter
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
import random
import math


# paypal imports.....
from django.conf import settings
#from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
import uuid



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
            mail_subject = 'AuctionHouse.in | Activate Your Account'
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
            messages.success(request, "Please confirm your email address to complete the registration.")
            return HttpResponseRedirect(reverse_lazy('auctions:login'))
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
        return HttpResponse('<h1>Activation link is invalid!</h1')


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
        if form.cleaned_data['image']:
            profile =form.save(commit=False)
            profile.user=models.User.objects.get(username=self.request.user)
            profile.user.profile_set()
            profile.save()
            return super().form_valid(form)
        else:
            return HttpResponseRedirect(reverse('home'))


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
                messages.success(request, "Your password sucessfully saved. Now do Login.")
                return HttpResponseRedirect(reverse_lazy('auctions:login'))

        return render(request, 'auctions/set_agent_password.html', {})

    return HttpResponse("Maybe Your password is already there.....")

class CurrentAuctionList(ListView):
    model = models.CurrentAuction
    template_name = "auctions/auction_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(current_auction_status=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        context['image_list'] = models.PropertyImagesUpload.objects.all()
        try:
            context['registered_user'] = models.RegForAuction.objects.all().filter(user=self.request.user)
        except:
            return context
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
        current_auction=get_object_or_404(models.CurrentAuction,pk=self.kwargs.get('pk'))
        try:
            context['registered_user'] = models.RegForAuction.objects.all().filter(user=self.request.user, current_auction_id=current_auction)
            print(context['registered_user'])
        except:
            pass
        context['past_bids']=auction_bid
        try:
            context['highest_bidder']=auction_bid[0]
        except:
            return context
        return context

    def post(self, request, *args, **kwargs):
        current_auction=get_object_or_404(models.CurrentAuction,pk=self.kwargs.get('pk'))
        title=self.request.POST['title']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=name=request.POST['email']
        mobile=request.POST['mobile']
        enquiry=request.POST['enquiry']
        enquiry_obj=models.MakeAnOffer.objects.create(property_id=current_auction.property_id,title=title,first_name=first_name,last_name=last_name,email=email,mobile=mobile,enquiry=enquiry)
        messages.success(self.request,"Enquiry is Submitted, We will contact you soon via email.",extra_tags='form_submitted')
        return HttpResponseRedirect(reverse_lazy('auctions:auction_detail', kwargs={'pk': current_auction.pk}))


class AuctionBid(LoginRequiredMixin,View):
    login_url = '/login/'

    def post(self,*args,**kwargs):
        current_auction_data =get_object_or_404(models.CurrentAuction,pk=self.kwargs.get('pk'))
        try:
            user = get_object_or_404(models.User, pk=self.request.user)
        except:
            print('not user')
            messages.error(self.request, "You Need to Register for auction in order to participate.",extra_tags='problem')
            return HttpResponseRedirect(reverse_lazy('auctions:auction_detail', kwargs={'pk': current_auction_data.pk}))


        register= models.RegForAuction.objects.all().filter(current_auction_id=self.kwargs.get('pk'))
        user = get_object_or_404(models.User, pk=self.request.user)
        for entry in register:
            if entry.user_id == user.user.pk:
                if entry.payment_status == "Completed":
                    if current_auction_data.next_bid <= float(self.request.POST['user_bid']):
                        bid_of_user = models.BiddingOfProperty.objects.create(current_auction_id=current_auction_data,user=user)
                        bid_of_user.user_bid_amount = float(self.request.POST['user_bid'])
                        bid_of_user.bid_time=timezone.now()
                        current_auction_data.current_amount = math.ceil(float(self.request.POST['user_bid']))
                        current_auction_data.highest_bidder=user
                        current_auction_data.bidding()
                        current_auction_data.save()
                        bid_of_user.save()
                        messages.success(self.request, "Your Bid is Submitted Successfully,Pls checkout the table to see your entry.",extra_tags='bid_done')
                        return HttpResponseRedirect(reverse_lazy('auctions:auction_detail', kwargs={'pk': current_auction_data.pk}))
                    else:
                        print("happend")
                        messages.error(self.request, "Please Enter the correct amount based on increment ratio.",extra_tags='problem')
                        return HttpResponseRedirect(reverse_lazy('auctions:auction_detail', kwargs={'pk': current_auction_data.pk}))
                else:
                    messages.error(self.request,"You have to register for participating in auction. Click on the Register for participating.",extra_tags='problem')
                    return HttpResponseRedirect(reverse_lazy('auctions:auction_detail', kwargs={'pk': current_auction_data.pk}))


        messages.error(self.request,"You have to register for participating in auction. Click on the Register for participating.",extra_tags='problem')
        return HttpResponseRedirect(reverse_lazy('auctions:auction_detail', kwargs={'pk': current_auction_data.pk}))

class UpcommingAuctionList(ListView):
    model = models.CurrentAuction
    template_name = "auctions/up_comming_auction_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(current_auction_status=False,scheduled_status=True,auction_finished_status=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        context['image_list'] = models.PropertyImagesUpload.objects.all()
        try:
            context['registered_user'] = models.RegForAuction.objects.all().filter(user=self.request.user)
        except:
            return context
        return context


class CheckingAuctionStatus(View):

    def get(self, request, *args, **kwargs):
        current_auction=get_object_or_404(models.CurrentAuction,pk=self.kwargs.get('pk'))
        current_auction_all=models.CurrentAuction.objects.all().filter(current_auction_status=False)
        if current_auction.current_ending_time <timezone.now():
            current_auction.auction_finished_status=True
            current_auction.current_auction_status=False
            print(current_auction.current_auction_status)
            current_auction.save()
        for auction in current_auction_all:
            print(auction.auction_start_date)
            print(timezone.now())
            if auction.auction_start_date < timezone.now() and auction.auction_finished_status==False and auction.scheduled_status== True:
                auction.current_auction_status=True
                auction.save()
            else:
                continue
        return HttpResponseRedirect(reverse_lazy('auctions:auction_detail', kwargs={'pk': current_auction.pk}))



# Views For Payments......

def process_payment(request, pk):
    current_auction = get_object_or_404(models.CurrentAuction, pk=pk)
    user = get_object_or_404(models.User, pk=request.user.pk)
    # register_auc = models.RegForAuction.objects.create(current_auction_id=current_auction, user=user)
    register_auc, created = models.RegForAuction.objects.get_or_create(current_auction_id=current_auction, user=user)
    if created == True:
        no = uuid.uuid1()
        register_auc.invoice_no = str(no.int)
    register_auc.save()
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': current_auction.registration_fees,
        'item_name': 'Register For Auction: {}'.format(register_auc.id),
        'invoice': str(register_auc.invoice_no),
        'currency_code': 'INR',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('auctions:payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('auctions:payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'auctions/process_payment.html', {'register_for_auction': register_auc, 'form': form})


@csrf_exempt
def payment_done(request):
    return render(request, 'auctions/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'auctions/payment_cancelled.html')

class FinishedAuctionList(ListView):
    model = models.CurrentAuction
    template_name = "auctions/finishedAuctions.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(current_auction_status=False, scheduled_status=True, auction_finished_status=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_list'] = models.PropertyImagesUpload.objects.all()
        try:
            context['registered_user'] = models.RegForAuction.objects.all().filter(user=self.request.user)
        except:
            return context
        return context


class RegisteredAuctionsList(LoginRequiredMixin, ListView):
    model = models.RegForAuction
    template_name = "auctions/user/reg_auction_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


def forgot_password_email(request):
    if request.method == "POST":
        email = request.POST.get('email')
        print(email)
        try:
            user_object = User.objects.get(email=email)
        except ObjectDoesNotExist:
            messages.error(request, 'Invaid Email!')
            return HttpResponseRedirect(reverse_lazy('auctions:forgot_password_email'))
        request.session['email'] = email
        request.session['user_id'] = user_object.id

        otp = ""

        for i in range(6):
            otp += str(random.randint(0,9))

        print(otp)
        request.session['otp'] = otp
        mail_subject = 'AuctionHouse.in | Forgot Password'
        message = render_to_string('auctions/render_forgot_password_email.html', {
            'user': user_object,
            'otp': otp
        })
        email = EmailMessage(
                    mail_subject, message, to=[email]
        )
        email.send()
        return HttpResponseRedirect(reverse_lazy('auctions:forgot_password_otp'))

    return render(request, 'auctions/user/forgot_password_email.html')

def forgot_password_otp(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        print(otp)

        if otp == request.session['otp']:
            return HttpResponseRedirect(reverse_lazy('auctions:new_password'))
        else:
            messages.error(request, 'Invalid OTP!')
            return HttpResponseRedirect(reverse_lazy('auctions:forgot_password_otp'))
    return render(request, "auctions/user/forgot_password_otp.html")

def new_password(request):
    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm password')

        if password == confirm_password:
            user_id = request.session['user_id']
            user = User.objects.get(pk=user_id)
            print(user.email)
            print(user.password)
            user.password = make_password(password)
            print(user.password)
            user.save()
            messages.success(request, 'Password Updated! Now do Login')
            return HttpResponseRedirect(reverse_lazy('auctions:login'))
        else:
            messages.error(request, 'Password does not match!')
            return HttpResponseRedirect(reverse_lazy('auctions:new_password'))
    return render(request, "auctions/user/new_password.html")

