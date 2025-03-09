from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .models import Reaction, Substance
from .forms import ReactionForm


class ReactionListView(LoginRequiredMixin, ListView):
    model = Reaction
    template_name = 'chembook/reaction_list.html'
    context_object_name = 'reactions'

class ReactionDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Reaction
    template_name = 'chembook/reaction_details.html'
    context_object_name = 'reaction'
    permission_required = 'chembook.view_reaction'

class ReactionCreateView(LoginRequiredMixin, CreateView):
    model = Reaction
    form_class = ReactionForm
    template_name = 'chembook/reaction_form.html'
    context_object_name = 'form'
    #permission_required = 'chembook.add_reaction'        #TODO: після впровадження управління дозволами розкоментувати

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('chembook:reaction_details', kwargs={'pk':self.object.pk})

class ReactionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Reaction
    form_class = ReactionForm
    template_name = 'chembook/reaction_form.html'
    context_object_name = 'form'
    permission_required = 'chembook.change_reaction'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['instance'] = self.object
        return kwargs

    def get_success_url(self):
        return reverse_lazy('chembook:reaction_details', kwargs={'pk':self.object.pk})

class ReactionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Reaction
    template_name = 'chembook/reaction_delete.html'
    context_object_name = 'reaction'
    permission_required = 'chembook.delete_reaction'
    success_url = reverse_lazy('chembook:reaction_list')
