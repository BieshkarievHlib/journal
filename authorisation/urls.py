from django.urls import path
from .views import *

app_name = 'authorisation'

urlpatterns = [
    path('register/', register,name='register'),
    path('login/', StandardLoginView.as_view(),name='login'),
    path('logout/', StandardLogoutView.as_view(),name='logout'),
    path('profile/', MyDetailsView.as_view(),name='profile')
]