from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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
    next_page = reverse_lazy('authorisation:login')

class MyDetailsView(LoginRequiredMixin, DetailView):
    model = StandardUser
    context_object_name = 'user'
    template_name = 'authorisation/user_details.html'

    def get_object(self):
        return self.request.user
