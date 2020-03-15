# from django.conf.urls import url,include
from django.urls import path,include
from . import views

app_name='auctions'

urlpatterns=[
    path(r'^signup/$',views.SignUp,name='singup'),
]
