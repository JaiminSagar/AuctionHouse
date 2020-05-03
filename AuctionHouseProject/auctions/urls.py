# from django.conf.urls import url,include
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

app_name='auctions'

urlpatterns=[

    path('signup/',views.signup,name='signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('forgot_password/email', views.forgot_password_email, name='forgot_password_email'),
    path('forgot_password/otp', views.forgot_password_otp, name='forgot_password_otp'),
    path('forgot_password/new_password', views.new_password, name='new_password'),
    
    path('login/',auth_views.LoginView.as_view(template_name='auctions/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),

    path('user/profile_detail/<int:pk>/',views.ProfileDetail.as_view(),name='profile_detail'),
    path('user/profile_update/<pk>/',views.ProfileUpdate.as_view(),name='profile_update'),
    path('user/profile_setup/',views.ProfileSetup.as_view(),name='setup_profile'),
    path('user/apply_evaluation/', views.ApplyEvaluation.as_view(), name='apply_evaluation'),
    path('user/evalution_list/', views.UserEvalutionList.as_view(), name='user_evaluation_list'),
    path('user/evaluation_list/property/<pk>/', views.PropertyDetailsForUser.as_view(), name='user_property_details'),
    path('user/registered_auctions/', views.RegisteredAuctionsList.as_view(), name='registered_auctions'),

    path('become_agent/', views.BecomeAgent.as_view(), name='become_agent'),
    path('agent/<pk>/set_password/', views.set_agent_password, name='agent_password'),
    path('agent/profile_details/<int:pk>',views.AgentDetailView.as_view(),name='agent_profile'),
    path('agent/profile_update/<pk>/',views.AgentUpdateView.as_view(),name='agent_update'),
    path('agent/evaluation_list/', views.EvaluationListForAgent.as_view(), name='agent_dashboard'),
    path('agent/evaluation_list/property/<pk>/', views.PropertyDetailsForAgent.as_view(), name='agent_property_details'),
    path('agent/evaluation_list/property/<pk>/add_description', views.add_property_description, name='add_description'),
    path('agent/evaluation_list/property/<pk>/add_files', views.propertyFilesUploadView, name='add_files'),
    path('agent/evaluation_list/property/<pk>/add_images', views.propertyImagesUploadView, name='add_images'),
    path('agent/evaluation_list/property/<pk>/submit', views.submit_property, name='submit_property'),

    path('auction_list/', views.AuctionList.as_view(), name='auction_list'),
    path('current_auctions/auction_bid/<int:pk>/',views.AuctionBid.as_view(),name='auction_bid'),
    path('upcomming_auctions/',views.UpcommingAuctionList.as_view(),name='upcomming_auction_list'),
    path('checking_auction_status/<pk>/',views.CheckingAuctionStatus.as_view(),name='check_auction_status'),
    path('current_auctions/',views.CurrentAuctionList.as_view(),name='current_auction_list'),
    path('auction_details/<int:pk>/',views.CurrentAuctionDetails.as_view(),name='auction_detail'),
    path('auction-details/<int:pk>/process_payment/', views.process_payment, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('finished_auctions',views.FinishedAuctionList.as_view(),name='finished_auctions'),
    

    # path('search/', FilterView.as_view(filterset_class=filters.AuctionFilter,template_name='index.html'), name='search'),
    # path('current_auctions/finsihed/<pk>/',views.AuctionFinished,name=''),


]
