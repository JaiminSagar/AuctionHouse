from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, ListView,UpdateView,View
from auctions.models import User,UserDetails
from auctions import forms, models
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import settings,get_user,get_user_model
from django.contrib import messages
from django.contrib.auth import get_user_model
from auctions.filters import AuctionFilter
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from auctions.tokens import account_activation_token
from django.contrib.auth.mixins import  LoginRequiredMixin

USER=get_user_model()

# email and activation related libraries
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
#from django.contrib.auth.models import User as Signup_User
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from auctions import forms
from django.contrib.auth.decorators import login_required


# Create your views here.
#

def checking(request):
        user=get_user(request)
        try:
            if user.agentuser.user_type == 'agent':
            # return HttpResponseRedirect(reverse('agent_home'))
                return HttpResponseRedirect(reverse('auctions:agent_dashboard'))
        except:
            try:
                if user.user.user_type == 'user':
                    if user.user.profile_setup == False:
                        print("hi")
                        return HttpResponseRedirect(reverse('auctions:setup_profile'))
                    else:
                        return HttpResponseRedirect(reverse('home'))
            except:
                try:
                    if user.auctionmanager.user_type == 'AuctionManager':
                        return HttpResponseRedirect(reverse('auction_approve_list'))
                except:
                    return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect("<h1>Something went Wrong</h1>")


# class AgentHome(TemplateView):
#     template_name = 'auctions/agent/agent_dashboard.html'



def adminLogin(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username, password)

        if username == 'admin@gmail.com' and password == 'admin@123':
            return HttpResponseRedirect(reverse('agent_list'))
        else:
            return HttpResponse('Invalid Email or password')
    return render(request, 'auctions/admin/admin_login.html', {})


class AgentList(LoginRequiredMixin,ListView):
    model = models.AgentUser
    template_name = 'auctions/admin/agent_approve_list.html'

@login_required
def approveAgent(request, pk):
    agent = get_object_or_404(models.AgentUser, pk=pk)
    agent.agent_approved()
    current_site = get_current_site(request)
    mail_subject = 'AuctionHouse.in | Agent Approved'
    message = render_to_string('auctions/agent_approved_email.html', {
        'agent': agent,
        'domain': current_site.domain,
    })
    to_email = agent.email
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.send()
    return redirect('agent_list')

class AuctionScheduling(LoginRequiredMixin,UpdateView):
    model = models.CurrentAuction
    template_name = 'auctions/admin/auction_scheduler.html'
    form_class = forms.SchedulAuctionForm

    def form_valid(self, form):
        print('abc')
        prop=form.save(commit=False)
        prop.scheduled()
        return super().form_valid(form)


class AuctionApprovalList(LoginRequiredMixin,ListView):
    model = models.PropertyReg
    template_name = 'auctions/admin/auctions_approve_list.html'

    def get_context_data(self, **kwargs):
        context =super().get_context_data()
        context['propertyreg_list']=context['propertyreg_list'].filter(approved=False,submitted=True)
        context['image_list']= models.PropertyImagesUpload.objects.all()
        print(context['image_list'])
        return context


class AuctionScheduleList(LoginRequiredMixin,ListView):
    model = models.CurrentAuction
    template_name = 'auctions/admin/schedule_list.html'

    def get_context_data(self, **kwargs):
        context =super().get_context_data()
        context['currentauction_list']=context['currentauction_list'].filter(scheduled_status=False)
        context['image_list']= models.PropertyImagesUpload.objects.all()
        return context

@login_required
def approve_auction(request,propertyid):
    propertyreg=get_object_or_404(models.PropertyReg,pk=propertyid)
    #print(propertyreg)
    propertyreg.approved_auction()
    current_auction=models.CurrentAuction.objects.create(property_id=propertyreg)
    current_auction.registration_fees = current_auction.property_id.pre_set_amount * (0.0001)
    current_auction.current_amount =current_auction.property_id.pre_set_amount
    current_auction.next_bid=current_auction.property_id.pre_set_amount+(current_auction.property_id.pre_set_amount*current_auction.increment_ratio)
    current_auction.save()
    propertyreg.save()
    return HttpResponseRedirect(reverse_lazy('auction_approve_list'))

class AuctionGuide(TemplateView):
    template_name = "auctions/AuctionGuide.html"


class Contact_us(TemplateView):
    template_name = 'auctions/contact_us.html'

    def post(self,*args,**kwargs):
        name=self.request.POST['name']
        email=self.request.POST['email']
        mobile=self.request.POST['phone']
        message=self.request.POST['message']
        contact_us_obj=models.ContactUs.objects.create(name=name,email=email,mobile=mobile,message=message)
        contact_us_obj.save()
        messages.success(self.request,"Form is Submitted.",extra_tags='form_submitted')
        return HttpResponseRedirect(reverse_lazy('contact_us'))

def AuctionManagerSignup(request):
    if request.method == 'POST':
        print("Entered")
        form = forms.CreateAuctionManager(request.POST)
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
            messages.success(request, "Please confirm your email address to complete the registration.")
            return HttpResponseRedirect(reverse_lazy('auctions:login'))
    else:
        form = forms.CreateAuctionManager()
    return render(request, 'auctions/signup_auction_manager.html', {'form': form})