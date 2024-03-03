from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages 
from BTMS import settings
import random
from django.contrib.auth.models import User 
from main.models import *

# Html email required stuff
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from main.models import * 


# Create your views here.
def home(request):
    carousel = Carousel.objects.all()
    routines = Routine.objects.filter(is_active=True)[:10]
    print(routines)
    params = {
        'carousel' : carousel,
        'routines' : routines,
    }
    return render(request,template_name='home.html',context=params)

def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        login_username = request.POST['email']
        login_password = request.POST['pass']
        try:
            user_email = User.objects.get(email=login_username)
            login_username = user_email
            user = authenticate(username=login_username, password=login_password)
        except:
            user = authenticate(username=login_username, password=login_password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in to BD Transports.")
            return redirect('/')

        elif not User.objects.filter(username=login_username).exists():
            messages.error(request, "There's no account exists for the given information.")
            return redirect('/login')
        
        elif not User.objects.get(username=login_username).is_active:
            usr = User.objects.get(username=login_username)
            otp = random.randint(100000, 999999)
            user_otp = OTP(username=User.objects.get(username=login_username), otp=otp)
            user_otp.save()
            # Html email start here
            greeting = f"Hello {usr.first_name} {usr.last_name}!"
            content = f"Your account is created successfully on BD Transports. Use this Otp to verify your account. This is a secret key. Don't share this key with anyother. In case of any problem contact the BD Transports admin.\nThanks!"
            context = {'greeting':greeting, 'content':content, 'otp':otp}
            html_content = render_to_string("email.html", context)
            text_content = strip_tags(html_content)
            send_email = EmailMultiAlternatives(
                "Welcome to BD Transports - Verify Your account",
                text_content,
                settings.EMAIL_HOST_USER,
                [usr.email],
                )
            send_email.attach_alternative(html_content, "text/html")
            send_email.send(fail_silently=False)
            return render(request, "signin.html", {'otp':True, 'user':usr})
            
        else:
            messages.error(request, "Invalid credential, please try again.")
            return render(request, 'signin.html')
    return render(request, template_name='signin.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        # get the post parameters
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        password_1 = request.POST['pass1']
        password_2 = request.POST['pass2']
        phone = request.POST['phone']
        gender = request.POST['gender']
        print(first_name,last_name,email,username,password_1,password_2,phone,gender)
        # Check for errors in input
        if User.objects.filter(username = username).first():
            messages.error(request, "This username is already taken")
            return redirect('/register')

        elif User.objects.filter(email = email).first():
            messages.error(request, "An account with this email already exists please try another.")
            return redirect('/register')

        # Create the user
        else:
            # creating user and saving it
            myuser = User.objects.create_user(username, email, password_1)
            myuser.is_active = False
            myuser.first_name = first_name
            myuser.last_name = last_name
            userinfo = Userdetail(user=User.objects.filter(username=username).first(), username=username, first_name=first_name, last_name=last_name, phone=phone)
            userinfo.save()
            myuser.save()
        #     # MAnaging OTP and sending
            usr = User.objects.get(username=username)
            otp = random.randint(100000, 999999)
            user_otp = OTP(username=User.objects.get(username=username), otp=otp)
            user_otp.save()
            # Html email start here
            greeting = f"Hello {first_name} {last_name}!"
            content = f"Your account has been created successfully on BD Transports. Use this Otp to verify your account. This is a secret key. Don't share this key with anyone. In case of any problem contact the BD Transports admin on our website.\nThanks!"
            context = {'greeting':greeting, 'content':content, 'otp':otp}
            html_content = render_to_string("email.html", context)
            text_content = strip_tags(html_content)
            send_email = EmailMultiAlternatives(
                "Welcome to BD Transports - Verify Your account",
                text_content,
                settings.EMAIL_HOST_USER,
                [email],
                )
            send_email.attach_alternative(html_content, "text/html")
            send_email.send(fail_silently=False)
        return render(request, "signup.html", {'otp':True, 'user':usr})
    return render(request, 'signup.html')

def contact(request):
    if request.method =="POST":
        first_name = request.POST.get('fname', '')
        last_name = request.POST.get('lname', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('prblm', '')
        contact = Contact(first_name=first_name, last_name=last_name, email=email, phone=phone, content=desc)
        contact.save()
        messages.success(request, "Your message has been sent.")
        return render(request, 'contact.html')
    return render(request,template_name='contact.html')

def routine(request):
    routines = Routine.objects.filter(is_active=True)
    params = {
        'routine' : routines,
    }
    return render(request,template_name='routine.html', context=params)

def book(request):
    return None

def otp_verifier(request):
    if request.method == "POST":
        get_otp = request.POST['otp']
        if get_otp:
            username = request.POST['user']
            usr = User.objects.get(username=username)
            my_user = User.objects.get(username=username)
            if int(get_otp) == OTP.objects.filter(username=usr).last().otp:
                my_user.is_active = True
                my_user.save()
                messages.success(request, "Your account is verified successfully.")
                return redirect('/login')
            else:
                messages.error(request, "The OTP you have entered is not correct.")
                return render(request, 'signup.html', {'otp':True, 'user':usr}) 
    return redirect('/')

def resend_otp(request):
    if request.method == "GET":
        user = request.GET['user']
        if User.objects.filter(username=user).exists() and not User.objects.get(username=user).is_active:
            usr = User.objects.get(username=user)
            otp = random.randint(100000, 999999)
            user_otp = OTP(username=User.objects.get(username=user), otp=otp)
            user_otp.save()
            # Html email start here
            greeting = f"Hello {usr.first_name} {usr.last_name}!"
            content = f"Your account is created successfully on BD Transports. Use this Otp to verify your account. This is a secret key. Don't share this key with anyother. In case of any problem contact the BD Transports admin on our website.\nThanks!"
            context = {'greeting':greeting, 'content':content, 'otp':otp}
            html_content = render_to_string("email.html", context)
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                "Welcome to BD Transports - Verify Your account",
                text_content,
                settings.EMAIL_HOST_USER,
                [usr.email],
                )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)
            return HttpResponse("Resend")
    return HttpResponse("Can't Send ")