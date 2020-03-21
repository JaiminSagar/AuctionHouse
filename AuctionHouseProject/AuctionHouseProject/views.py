from django.shortcuts import render
from django.views.generic import TemplateView,CreateView
from auctions.models import User
from auctions import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# Create your views here.

# class HomePage(CreateView):
#     template_name = 'index.html'
#     form_class = forms.ProfileSetupForm
#     success_url = reverse_lazy('auctions:profile_update')
#     template_name = 'index.html'
#     users =User.objects.all()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['users'] = self.users
#         # context['form']=forms.ProfileSetupForm()
#         return context


class ThanksPage(TemplateView):
    template_name = 'thanks.html'


class HomePage(TemplateView):
    template_name = 'index.html'
    form_class =forms.ProfileSetupForm
    users =User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = self.users
        context['form']=forms.ProfileSetupForm()
        return context

    # def post(self, request, *args, **kwargs):
    #     # pk=request.
        # if form.is_valid():
        #     form.save()
        #     return HttpResponseRedirect(reverse('auctions:post_detail'))
        # else:
        #     return render(request, self.template_name, {'form': form})