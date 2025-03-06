from django.urls import path
from . import views

app_name = 'chembook'

urlpatterns = [
    path('reactions/', views.reaction_list, name='reaction_list'),
    path('reactions/<int:pk>', views.reaction_details, name='reaction_details'),
    path('reactions/new', views.reaction_edit,name='reaction_create'),
    path('reactions/<int:pk>/edit', views.reaction_edit, name='reaction_edit'),
    path('reactions/<int:pk>/delete', views.reaction_delete,name='reaction_delete'),
]