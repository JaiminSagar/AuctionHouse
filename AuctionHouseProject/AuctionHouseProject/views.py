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
class HomePage(CreateView):
    template_name = 'index.html'
    form_class = forms.ProfileSetupForm
    model = UserDetails
    # success_url = reverse_lazy('auctions:profile_update')
    # template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form']=self.form_class
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            user_from=get_user(request)
            user=User.objects.get(pk=user_from.pk)
            form.save(commit=False)
            form.user.user=user
            # form.user=user_from.username
            print(form)
            form.save()
            # address = form.cleaned_data['address']
            # mobile = form.cleaned_data['mobile']
            # city = form.cleaned_data['city']
            # state = form.cleaned_data['state']
            # pincode = form.cleaned_data['pincode']
            # image = form.cleaned_data['image']
            # # first_name = form.cleaned_data['first_name']
            # # last_name = form.cleaned_data['last_name']
            print(type(user_from),type(user.username),user.username,user.user.username,user_from.pk,user.pk)#address,mobile,city,image,state,pincode
            return HttpResponseRedirect('auctions/logout')




class ThanksPage(TemplateView):
    template_name = 'thanks.html'

