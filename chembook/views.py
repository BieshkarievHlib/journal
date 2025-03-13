from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden


from .models import Reaction, Substance, Batch, BatchSubstance
from .forms import ReactionForm, BatchForm, BatchSubstanceFormSet


class ReactionListView(LoginRequiredMixin, ListView):
    model = Reaction
    template_name = 'chembook/reaction_list.html'
    context_object_name = 'reactions'

@permission_required('chembook.change_reaction', raise_exception=True)
def reaction_edit(request, reaction_pk=None):
    if reaction_pk:
        reaction = get_object_or_404(Reaction, pk=reaction_pk)
    else: 
        reaction = None

    if request.method == 'POST':
        form = ReactionForm(request.POST, user=request.user, instance=reaction)
        if form.is_valid():
            reaction = form.save()
            return redirect('chembook:reaction_details', reaction_pk=reaction.pk)
    else:
        form = ReactionForm(user=request.user, instance=reaction)

    return render(request, 'chembook/reaction_form.html', {'form':form})

class ReactionDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Reaction
    template_name = 'chembook/reaction_details.html'
    context_object_name = 'reaction'
    permission_required = 'chembook.view_reaction'

    def get_object(self):
        return get_object_or_404(Reaction, pk=self.kwargs['reaction_pk'])

    def has_permission(self):
        reaction = self.get_object()
        return self.request.user.has_perm(self.permission_required, reaction)

class ReactionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Reaction
    template_name = 'chembook/reaction_delete.html'
    context_object_name = 'reaction'
    permission_required = 'chembook.delete_reaction'
    success_url = reverse_lazy('chembook:reaction_list')

    def get_object(self):
        return get_object_or_404(Reaction, pk=self.kwargs['reaction_pk'])

    def has_permission(self):
        reaction = self.get_object()
        return self.request.user.has_perm(self.permission_required, reaction)

def batch_edit(request, reaction_pk, batch_pk = None):                                  #TODO: Додати до всіх бетчviews підтримку дозволів
    if batch_pk and request.user.has_perm('chembook.change_batch', Batch.objects.get(pk=batch_pk)):
        batch = get_object_or_404(Batch, pk=batch_pk)
    elif not batch_pk and request.user.has_perm('chembook.add_batch', Reaction.objects.get(pk=reaction_pk)):
        batch = None
    else: 
        return HttpResponseForbidden('У Вас немає прав доступу для додавання або редагування бетчів цієї реакції.')

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
        #print(f'Form (or formset) is invalid! Errors: {form.errors}')
    else:
        form = BatchForm(user=request.user, reaction=reaction_pk, instance=batch)
        formset = BatchSubstanceFormSet(instance=batch)

        return render(request, 'chembook/batch_form.html', {'form':form, 'formset':formset})

class BatchDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Batch
    context_object_name = 'batch'
    template_name = 'chembook/batch_details.html'
    permission_required='chembook.view_batch'

    def has_permission(self):
        return self.request.user.has_perm('chembook.view_batch', self.get_object())

    def get_object(self):
        return get_object_or_404(Batch, pk=self.kwargs['batch_pk'], reaction__pk=self.kwargs['reaction_pk'])

class BatchDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model=Batch
    template_name = 'chembook/batch_delete.html'
    context_object_name = 'batch'
    permission_required = 'chembook.delete_batch'

    def has_permission(self):
        return self.request.user.has_perm('chembook.delete_batch', self.get_object())

    def get_object(self):
        return get_object_or_404(Batch, pk=self.kwargs['batch_pk'])

    def get_success_url(self):
        return reverse_lazy('chembook:reaction_details', kwargs={'reaction_pk':self.kwargs['reaction_pk']})

    











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
#
#_____________________________________________________Це працює, але більше не потрібно. Видалять жавко, най поки буде шпаргалкою для CBV__________________________________________________________
#class ReactionCreateView(LoginRequiredMixin, CreateView):
#    model = Reaction
#    form_class = ReactionForm
#    template_name = 'chembook/reaction_form.html'
#    context_object_name = 'form'
#
#    def get_form_kwargs(self):
#        kwargs = super().get_form_kwargs()
#        kwargs['user'] = self.request.user
#        return kwargs
#
#    def get_success_url(self):
#        return reverse_lazy('chembook:reaction_details', kwargs={'pk':self.object.pk})
#
#class ReactionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#    model = Reaction
#    form_class = ReactionForm
#    template_name = 'chembook/reaction_form.html'
#    context_object_name = 'form'
#    permission_required = 'chembook.change_reaction'
#
#    def has_permission(self):
#        reaction = self.get_object()
#        return self.request.user.has_perm(self.permission_required, reaction)
#
#    def get_form_kwargs(self):
#        kwargs = super().get_form_kwargs()
#        kwargs['user'] = self.request.user
#        kwargs['instance'] = self.object
#        return kwargs
#
#    def get_success_url(self):
#        return reverse_lazy('chembook:reaction_details', kwargs={'pk':self.object.pk})