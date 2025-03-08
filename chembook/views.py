from django.shortcuts import render, get_object_or_404, redirect
from .models import Reaction, Substance
from .forms import ReactionForm
from django.http import Http404

def reaction_list(request):
    reactions = Reaction.objects.all()
    return render(request, 'chembook/reaction_list.html', context={'reactions':reactions})

def reaction_details(request, pk):
    reaction = get_object_or_404(Reaction, pk=pk)
    return render(request, 'chembook/reaction_details.html', context={'reaction':reaction})

def reaction_edit(request, pk=None):
    if pk:
        reaction = get_object_or_404(Reaction, pk=pk)
    else:
        reaction = None

    if request.method == 'POST':
        form = ReactionForm(request.POST, instance=reaction)
        if form.is_valid():
            reaction = form.save()
            return redirect('chembook:reaction_details', pk=reaction.pk)
    else:
        form = ReactionForm(instance=reaction)

    return render(request, 'chembook/reaction_form.html', {'form':form})

def reaction_delete(request, pk):
    reaction = get_object_or_404(Reaction, pk=pk)
    if request.method == 'POST':
        reaction.delete()  
        return redirect('chembook:reaction_list')
    else:
        return render(request, 'chembook/reaction_delete.html', {'reaction':reaction})