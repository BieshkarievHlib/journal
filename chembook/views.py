from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden


from .models import Reaction, Substance, Batch, BatchSubstance, Synthesis, Pathway
from .forms import ReactionForm, BatchForm, BatchSubstanceFormSet, SynthesisForm, StageFormSet, PathwayForm


class ReactionListView(LoginRequiredMixin, ListView):
    model = Reaction
    template_name = 'chembook/reaction_list.html'
    context_object_name = 'reactions'

#TODO: Додати перевірку user.has_perm() в if-else statement: прив'язка до синтезу буде необов'язкова
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

def batch_edit(request, reaction_pk, batch_pk = None):
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

class SynthesisListView(LoginRequiredMixin, ListView):
    model = Synthesis
    template_name = 'chembook/synthesis_list.html'
    context_object_name = 'syntheses'

class SynthesisDetailsView(DetailView):
    model = Synthesis
    template_name = 'chembook/synthesis_details.html'
    context_object_name = 'synthesis'

    def get_object(self):
        return get_object_or_404(Synthesis, pk=self.kwargs['synthesis_pk'])
    
def synthesis_edit(request, synthesis_pk=None):
    if synthesis_pk:
        synthesis = get_object_or_404(Synthesis, pk=synthesis_pk)
    else:
        synthesis = None

    if request.method == 'POST':
        form = SynthesisForm(request.POST, user=request.user, instance=synthesis)
        if form.is_valid():
            synthesis = form.save()
            return redirect('chembook:synthesis_details', synthesis_pk=synthesis.pk)
    else:
        form = SynthesisForm(user=request.user, instance=synthesis)
        
    return render(request, 'chembook/synthesis_form.html', {'form':form})

class SynthesisDeleteView(DeleteView):
    model = Synthesis
    template_name = 'chembook/synthesis_delete.html'
    context_object_name = 'synthesis'
    #permission_required = 'chembook.delete_synthesis'
    success_url = reverse_lazy('chembook:synthesis_list')

    def get_object(self):
        return get_object_or_404(Synthesis, pk=self.kwargs['synthesis_pk'])

def pathway_edit(request, synthesis_pk, pathway_pk = None):
    if pathway_pk:
        pathway = get_object_or_404(Pathway, pk=pathway_pk)
    elif not pathway_pk:
        pathway = None

    if request.method == 'POST':
        form = PathwayForm(request.POST,synthesis=synthesis_pk, instance=pathway)
        formset = StageFormSet(request.POST, instance=pathway)
        if form.is_valid() and formset.is_valid():
            pathway = form.save(commit=False)
            formset.instance = pathway
            pathway.save()
            formset.save()
            return redirect('chembook:synthesis_details', synthesis_pk=synthesis_pk)
        print(f'Form (or formset) is invalid! Errors: {form.errors}, {formset.errors}')
    else:
        form = PathwayForm(synthesis=synthesis_pk, instance=pathway)
        formset = StageFormSet(instance=pathway)

    return render(request, 'chembook/pathway_form.html', {'form':form, 'formset':formset})

class PathwayDetailsView(DetailView):
    model = Pathway
    template_name = 'chembook/pathway_details.html'
    context_object_name = 'pathway'

    def get_object(self):
        return get_object_or_404(Pathway, pk=self.kwargs['pathway_pk'], synthesis__pk=self.kwargs['synthesis_pk'])







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