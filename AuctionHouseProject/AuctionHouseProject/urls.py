"""AuctionHouseProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
# from auctions import views as viewer
from . import views
from django.conf import settings
from django.conf.urls.static import static
from auctions import filters
from django_filters.views import FilterView


urlpatterns = [
    path('',views.checking,name='profile_check'),
    path('admin/', admin.site.urls),
    path('home/',FilterView.as_view(filterset_class=filters.AuctionFilter,template_name='index.html'),name='home'),
    # path('agent/dashboard',views.AgentHome.as_view(),name='agent_home'),
    path('auctions/',include('auctions.urls',namespace='auctions')),
    # path('thanks/', views.ThanksPage.as_view(), name='thanks'),
    # path('admin_login/', views.adminLogin, name='admin_login'),
    path('agent_list/', views.AgentList.as_view(), name='agent_list'),
    path('agent_list/approve/<pk>/', views.approveAgent, name='approve_agent'),
    path('auction_approval_list/',views.AuctionApprovalList.as_view(),name='auction_approve_list'),
    path('schedule_list/',views.AuctionScheduleList.as_view(),name='schedule_list'),
    path('schedule_auction/<pk>/', views.AuctionScheduling.as_view(),name='schedule_auction'),
    path('approve_auction/<int:propertyid>/',views.approve_auction,name='approve_auction'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('auction_guide',views.AuctionGuide.as_view(),name='auction_guide'),
    path('contact_us/',views.Contact_us.as_view(),name='contact_us'),
    path('create_auction_manager/',views.AuctionManagerSignup,name='auction_manager_signup'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)