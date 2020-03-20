from django.shortcuts import render
from django.views.generic import TemplateView
from auctions.models import User
# Create your views here.

class HomePage(TemplateView):
    template_name = 'index.html'
    # context_object_name = 'post_draft_list'
    # chkuser =User.objects.all()
    #
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['user'] = self.chkuser
    #     return context
# class TestPage(TemplateView):
#     template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'
