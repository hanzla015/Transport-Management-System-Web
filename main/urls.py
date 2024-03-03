from django.urls import path
from main.views import *

urlpatterns = [
    path('',home,name="Home"),
    path('login',signin,name="Sign In"),
    path('register',register,name="Sign In"),
    path('contact',contact,name="Contact"),
    path('routines',routine,name="Routine"),
    path('book',book,name="book"),
    path('account-activation', otp_verifier, name='account-activation'),

   
]
