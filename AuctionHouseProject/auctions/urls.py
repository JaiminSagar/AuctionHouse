# from django.conf.urls import url,include
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

app_name='auctions'

urlpatterns=[
    path('signup/',views.SignUp.as_view(),name='signup'),
<<<<<<< HEAD
    path('become_agent/', views.BecomeAgent.as_view(), name='become_agent'),
    path('login/',auth_views.LoginView.as_view(template_name='auctions/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='index.html'),name='logout'),
    path('thanks/', views.Thanks.as_view(), name='thanks'),
=======
    path('login/',auth_views.LoginView.as_view(template_name='auctions/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='index.html'),name='logout'),
>>>>>>> f27093f459a4e642b248d5417a1d9ce369f828c8
    # path('home/',views.Welcome.as_view(),name='userhome')
]
