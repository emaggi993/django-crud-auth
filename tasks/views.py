from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
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
    tasks = Task.objects.filter(user= request.user)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

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
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form= TaskForm(request.POST)
            new_task= form.save(commit=False)
            new_task.user = request.user
            print(new_task)
            new_task.save()
            
        except:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': "Ingrese datos correctos"
            })
        else:
            return redirect("tasks")