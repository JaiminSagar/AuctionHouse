# from django.conf.urls import url,include
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from . import views

app_name='auctions'

urlpatterns=[

    path('signup/',views.signup,name='signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('become_agent/', views.BecomeAgent.as_view(), name='become_agent'),
    path('login/',auth_views.LoginView.as_view(template_name='auctions/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('profile_detail/<int:pk>/',views.ProfileDetail.as_view(),name='profile_detail'),
    path('profile_update/<pk>/',views.ProfileUpdate.as_view(),name='profile_update'),
    path('profile_setup/',views.ProfileSetup.as_view(),name='setup_profile'),
    path('auction_list/', views.AuctionList.as_view(), name='auction_list'),
    path('agent/<pk>/set_password/', views.set_agent_password, name='agent_password'),
    path('agent/profile_details/<int:pk>',views.AgentDetailView.as_view(),name='agent_profile'),
    path('agent/profile_update/<pk>/',views.AgentUpdateView.as_view(),name='agent_update'),
    path('user/apply_evaluation/', views.ApplyEvaluation.as_view(), name='apply_evaluation'),
    path('user/evalution_list/', views.UserEvalutionList.as_view(), name='user_evaluation_list'),
    path('agent/evaluation_list/', views.EvaluationListForAgent.as_view(), name='agent_dashboard'),


]
