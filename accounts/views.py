from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.http import HttpResponse


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # password validation
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'E-mail is already taken ')
                    return redirect('register')
                else:       # everything Ok
                     user = User.objects.create_user(username=username, password=password, email=email,
                     first_name=first_name, last_name=last_name)
                     #Login after register
                     # auth.login(request, user)
                     # messages.success(request, 'Successfully logged in')
                     # return redirect('index')
                     user.save()
                     messages.success(request, 'Successfully registered')
                     messages.success(request, 'Now you can log in')
                     return redirect('login')

        else:
            messages.error(request,'Passwords do not match')
            return redirect('register')
    else:
        return render(request, "accounts/register.html")



def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Successfully Logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')



def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, 'Successfully logged out')
        return redirect('login')







