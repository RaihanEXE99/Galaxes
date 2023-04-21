from django.conf.urls import url
from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('registration_view/', views.registration_view, name="registration_view"),
    path('signIn_view/', views.signIn_view, name="signIn_view"),
    path('logout_view/', views.logout_view, name="logout_view"),
    path('sampleFuture/<str:title>', views.sampleFuture, name="sampleFuture"),
    path('home_view/', views.home_view, name="home_view"), # Beta Test URL
    
]