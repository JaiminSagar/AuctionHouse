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

USER=get_user_model()

# email and activation related libraries
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
#from django.utils.encoding import force_bytes, force_text
#from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
#from .tokens import account_activation_token
#from django.contrib.auth.models import User as Signup_User
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
#

def checking(request):
        user=get_user(request)
        if user.is_staff:
            # return HttpResponseRedirect(reverse('agent_home'))
            return HttpResponseRedirect(reverse('auctions:agent_dashboard'))
        elif user.is_staff == False:
            try:
                if user.user.profile_setup == False:
                    print("hi")
                    return HttpResponseRedirect(reverse('auctions:setup_profile'))
                else:
                    return HttpResponseRedirect(reverse('home'))
            except:
                return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect("<h1>Something went Wrong</h1>")

class HomePage(TemplateView):
    template_name = 'index.html'

# class AgentHome(TemplateView):
#     template_name = 'auctions/agent/agent_dashboard.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

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

class AgentList(ListView):
    model = models.AgentUser
    template_name = 'auctions/admin/agent_approve_list.html'


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

class AuctionScheduling(UpdateView):
    model = models.CurrentAuction
    template_name = 'auctions/admin/auction_scheduler.html'
    form_class = forms.SchedulAuctionForm

    def form_valid(self, form):
        prop=form.save(commit=False)
        prop.scheduled()
        return super().form_valid(form)


class AuctionApprovalList(ListView):
    model = models.PropertyReg
    template_name = 'auctions/admin/auctions_approve_list.html'

    def get_context_data(self, **kwargs):
        context =super().get_context_data()
        context['propertyreg_list']=context['propertyreg_list'].filter(approved=False,submitted=True)
        context['image_list']= models.PropertyImagesUpload.objects.all()
        return context


class AuctionScheduleList(ListView):
    model = models.CurrentAuction
    template_name = 'auctions/admin/schedule_list.html'

    def get_context_data(self, **kwargs):
        context =super().get_context_data()
        context['currentauction_list']=context['currentauction_list'].filter(scheduled_status=False)
        context['image_list']= models.PropertyImagesUpload.objects.all()
        return context

def approve_auction(request,propertyid):
    propertyreg=get_object_or_404(models.PropertyReg,pk=propertyid)
    propertyreg.approved_auction()
    current_auction=models.CurrentAuction.objects.create(property_id=propertyreg)
    current_auction.registration_fees = current_auction.property_id.pre_set_amount * (0.01)
    current_auction.save()
    propertyreg.save()
    return HttpResponseRedirect(reverse_lazy('auction_approve_list'))