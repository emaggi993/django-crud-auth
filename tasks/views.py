from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
# Create your views here.


def signup(request):
    if request.method == 'GET':

        return render(request, "signup.html", {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/tasks/')
            except:
                return render(request, "signup.html", {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        else:
            return render(request, "signup.html", {
                'form': UserCreationForm,
                'error': 'Las contraseñas no coinciden'
            })
def tasks(request):
    return render(request, 'tasks.html')

def home(request):
    return render(request, 'home.html')
def signout(request):
    logout(request)
    return redirect("/")
def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate( request, username= request.POST['username'], password= request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect('/tasks')