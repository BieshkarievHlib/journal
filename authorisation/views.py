from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import StandardUserCreationForm, StandardLoginForm
from .models import StandardUser

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = StandardUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chembook:reaction_list')
    else:
        form = StandardUserCreationForm()
        return render(request, 'authorisation/register.html', {'form':form})

class StandardLoginView(LoginView):
    template_name = 'authorisation/login.html'
    authentication_form = StandardLoginForm
    
    next_page = reverse_lazy('chembook:reaction_list')

class StandardLogoutView(LogoutView):
    next_page = reverse_lazy('chembook:reaction_list')