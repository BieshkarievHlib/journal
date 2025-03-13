from django.urls import path
from . import views

app_name = 'chembook'

urlpatterns = [
    path('synthesis/', views.SynthesisListView.as_view(),name='synthesis_list'),
    path('synthesis/<int:synthesis_pk>', views.SynthesisDetailsView.as_view(), name='synthesis_details'),
    path('synthesis/new', views.synthesis_edit,name='synthesis_create'),
    path('synthesis/<int:synthesis_pk>/edit', views.synthesis_edit,name='synthesis_edit'),
    path('synthesis/<int:synthesis_pk>/pathway/new', views.pathway_edit,name='pathway_create'),
    path('synthesis/<int:synthesis_pk>/pathway/<int:pathway_pk>', views.pathway_edit,name='pathway_edit'),
    path('reactions/', views.ReactionListView.as_view(), name='reaction_list'),
    path('reactions/<int:reaction_pk>', views.ReactionDetailsView.as_view(), name='reaction_details'),
    path('reactions/new', views.reaction_edit, name='reaction_create'),
    path('reactions/<int:reaction_pk>/edit', views.reaction_edit, name='reaction_edit'),
    path('reactions/<int:reaction_pk>/delete', views.ReactionDeleteView.as_view(),name='reaction_delete'),
    path('reactions/<int:reaction_pk>/batches/new', views.batch_edit,name='batch_create'),
    path('reactions/<int:reaction_pk>/batches/<int:batch_pk>/edit', views.batch_edit,name='batch_edit'),
    path('reactions/<int:reaction_pk>/batches/<int:batch_pk>', views.BatchDetailsView.as_view(),name='batch_details'),
    path('reactions/<int:reaction_pk>/batches/<int:batch_pk>/delete',views.BatchDeleteView.as_view(),name='batch_delete')
]