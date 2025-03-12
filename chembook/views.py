from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render

from .models import Reaction, Substance, Batch, BatchSubstance
from .forms import ReactionForm, BatchForm, BatchSubstanceFormSet


class ReactionListView(LoginRequiredMixin, ListView):
    model = Reaction
    template_name = 'chembook/reaction_list.html'
    context_object_name = 'reactions'

class ReactionDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Reaction
    template_name = 'chembook/reaction_details.html'
    context_object_name = 'reaction'
    permission_required = 'chembook.view_reaction'

    def has_permission(self):
        reaction = self.get_object()
        return self.request.user.has_perm(self.permission_required, reaction)

class ReactionCreateView(LoginRequiredMixin, CreateView):
    model = Reaction
    form_class = ReactionForm
    template_name = 'chembook/reaction_form.html'
    context_object_name = 'form'

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

    def has_permission(self):
        reaction = self.get_object()
        return self.request.user.has_perm(self.permission_required, reaction)

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

    def has_permission(self):
        reaction = self.get_object()
        return self.request.user.has_perm(self.permission_required, reaction)

def batch_edit(request, reaction_pk, batch_pk = None):                                  #TODO: Додати до всіх бетчviews підтримку дозволів
    if batch_pk:
        batch = get_object_or_404(Batch, pk=batch_pk)
    else:
        batch = None



    if request.method == 'POST':
        form = BatchForm(request.POST, user=request.user, reaction=reaction_pk, instance=batch)
        formset = BatchSubstanceFormSet(request.POST, instance=batch)
        if form.is_valid() and formset.is_valid():
            batch = form.save(commit=False)
            formset.instance = batch

            reaction = Reaction.objects.get(pk=reaction_pk)
            for substance in reaction.substances.all():
                BatchSubstance.objects.get_or_create(batch=batch, substance=substance)
            
            batch.save()
            formset.save()
            return redirect('chembook:batch_details',reaction_pk=reaction_pk, batch_pk=batch.pk)
        print(f'Form (or formset) is invalid! Errors: {form.errors}')
    else:
        form = BatchForm(user=request.user, reaction=reaction_pk, instance=batch)
        formset = BatchSubstanceFormSet(instance=batch)

        return render(request, 'chembook/batch_form.html', {'form':form, 'formset':formset})

class BatchDetailsView(DetailView):
    model = Batch
    context_object_name = 'batch'
    template_name = 'chembook/batch_details.html'

    def get_object(self):
        return get_object_or_404(Batch, pk=self.kwargs['batch_pk'], reaction__pk=self.kwargs['reaction_pk'])















#___________________________________________________Колись я перероблю це так, шоб воно працювало. Колись...___________________________________________________________________________________________________
#class BatchCreateView(CreateView):                 
#    model = Batch
#    form_class = BatchForm
#    template_name = 'chembook/batch_form.html'
#    context_object_name = 'form'
#
#    def get_form_kwargs(self):
#        kwargs = super().get_form_kwargs()
#        reaction_pk = self.kwargs.get('reaction_pk')
#        kwargs['user'] = self.request.user
#        kwargs['reaction'] = get_object_or_404(Reaction, pk=reaction_pk)
#        return kwargs
#    
#    def form_valid(self, form):
#        self.object.form.save(commit=False)
#        self.object.reaction = self.reaction
#        self.object.save()
#
#        return super().form_valid(form)
#    
#    def get_success_url(self):
#        return reverse_lazy('chembook:reaction_details', kwargs={'pk':self.object.reaction.pk})