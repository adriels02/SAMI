from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .forms import LoginForm , RegisterForm
               
def register(request):
    if request.method == "GET":
        context = {}
        return render(request, "management/register.html", context)
    else: 
        form = RegisterForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']

            if password != password_confirm:
                form.add_error('password_confirm', 'As senhas não coincidem')
    
            elif User.objects.filter(email=email).first():
                form.add_error('email', 'Email já cadastrado')
            else:
                user = User.objects.create_user(username=email, email=email, password=password)
                user.first_name = fullname
                user.save() 
                return redirect(reverse('management:logar'))
        else: 
            form = RegisterForm()
        return render(request, "management/register.html", {'form': form})
    
def logar(request):
    if request.method == "GET":
     context = {}
     return render(request, "management/logar.html", context)
    
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(username= email, password = password)
        
            if user is not None:
                login(request, user)
                return redirect(reverse('maintenance:home'))
            else:
                form.add_error(None, 'Credenciais inválidas')
            
        else:
            form = LoginForm()
        return render(request, "management/logar.html", {'form': form})    