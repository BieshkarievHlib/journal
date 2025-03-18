from django.urls import path

from . import views

app_name = 'chemhub'

urlpatterns = [
    path('synthesis/', views.SynthesisListView.as_view(),name='synthesis_list'),
    path('synthesis/<int:synthesis_pk>', views.SynthesisDetailsView.as_view(), name='synthesis_details'),
    path('synthesis/new', views.synthesis_edit,name='synthesis_create'),
    path('synthesis/<int:synthesis_pk>/edit', views.synthesis_edit,name='synthesis_edit'),
    path('synthesis/<int:synthesis_pk>/pathway/new', views.pathway_edit,name='pathway_create'),
    path('synthesis/<int:synthesis_pk>/pathway/<int:pathway_pk>/edit', views.pathway_edit,name='pathway_edit'),
    path('synthesis/<int:synthesis_pk>/pathway/<int:pathway_pk>/delete', views.PathwayDeleteView.as_view(),name='pathway_delete'),
]