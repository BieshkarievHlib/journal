from django.urls import path
from . import views

app_name = 'chembook'

urlpatterns = [
    path('reactions/', views.ReactionListView.as_view(), name='reaction_list'),
    path('reactions/<int:pk>', views.ReactionDetailsView.as_view(), name='reaction_details'),
    path('reactions/new', views.ReactionCreateView.as_view(), name='reaction_create'),
    path('reactions/<int:pk>/edit', views.ReactionUpdateView.as_view(), name='reaction_edit'),
    path('reactions/<int:pk>/delete', views.ReactionDeleteView.as_view(),name='reaction_delete'),
]