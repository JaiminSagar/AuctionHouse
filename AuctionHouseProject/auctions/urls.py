# from django.conf.urls import url,include
from django.urls import path,include
from . import views

app_name='auctions'

urlpatterns=[
    path('signup/',views.SignUp.as_view(),name='signup'),
]
