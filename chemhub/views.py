from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView

from .models import Synthesis, Stage, Pathway
from .forms import SynthesisForm, PathwayForm, StageFormSet

class SynthesisListView(LoginRequiredMixin, ListView):
    model = Synthesis
    template_name = 'chemhub/synthesis_list.html'
    context_object_name = 'syntheses'

class SynthesisDetailsView(DetailView):
    model = Synthesis
    template_name = 'chemhub/synthesis_details.html'
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
            return redirect('chemhub:synthesis_details', synthesis_pk=synthesis.pk)
    else:
        form = SynthesisForm(user=request.user, instance=synthesis)
        
    return render(request, 'chemhub/synthesis_form.html', {'form':form})

class SynthesisDeleteView(DeleteView):
    model = Synthesis
    template_name = 'chemhub/synthesis_delete.html'
    context_object_name = 'synthesis'
    #permission_required = 'chemhub.delete_synthesis'
    success_url = reverse_lazy('chemhub:synthesis_list')

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
            return redirect('chemhub:synthesis_details', synthesis_pk=synthesis_pk)
        print(f'Form (or formset) is invalid! Errors: {form.errors}, {formset.errors}')
    else:
        form = PathwayForm(synthesis=synthesis_pk, instance=pathway)
        formset = StageFormSet(instance=pathway)

    return render(request, 'chemhub/pathway_form.html', {'form':form, 'formset':formset})

class PathwayDeleteView(DeleteView):
    model = Pathway
    template_name = 'chemhub/pathway_delete.html'
    context_object_name = 'pathway'

    def get_object(self):
        return get_object_or_404(Pathway, pk=self.kwargs['pathway_pk'],synthesis__pk=self.kwargs['synthesis_pk'])

    def get_success_url(self):
        return reverse_lazy('chemhub:synthesis_list')