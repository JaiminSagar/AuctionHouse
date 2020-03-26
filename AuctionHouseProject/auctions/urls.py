# from django.conf.urls import url,include
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

app_name='auctions'

urlpatterns=[

    path('signup/',views.SignUp.as_view(),name='signup'),
    path('become_agent/', views.BecomeAgent.as_view(), name='become_agent'),
    path('login/',auth_views.LoginView.as_view(template_name='auctions/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('profile_detail/<int:id>/',views.ProfileDetail.as_view(),name='profile_detail'),
    path('profile_update/<pk>/',views.ProfileUpdate.as_view(),name='update'),
    path('profile_setup/',views.ProfileSetup.as_view(),name='setup_profile'),


]
