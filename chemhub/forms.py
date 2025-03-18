from django.forms import ModelForm, inlineformset_factory

from .models import Synthesis, Stage, Pathway
from guardian.shortcuts import assign_perm

class SynthesisForm(ModelForm):
    class Meta:
        model = Synthesis
        fields = [
            'name',
            'description',
            'main_product',
            'number_of_stages'
        ]

    def __init__(self, *args, user = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    
    def save(self,commit=True):
        synthesis = super().save(commit=False)

        if not synthesis.author and self.user:
            synthesis.save()
            synthesis.author = self.user
            
            assign_perm('add_pathway',synthesis.author, synthesis)
            assign_perm('view_synthesis', synthesis.author, synthesis)
            assign_perm('delete_synthesis', synthesis.author, synthesis)
            assign_perm('change_synthesis', synthesis.author, synthesis)
        
        if commit:
            synthesis.save()
        
        return synthesis
    
class PathwayForm(ModelForm):
    class Meta:
        model = Pathway
        fields = [
            'synthesis'
        ]

    def __init__(self, *args, synthesis=None, **kwargs):
        super().__init__(*args,**kwargs)
        self.synthesis = synthesis

    def save(self,commit=True):
        pathway = super().save(commit=False)
        pathway.synthesis = Synthesis.objects.get(pk=self.synthesis)
        pathway.save()

        if commit:
            pathway.save()
        
        return pathway

StageFormSet = inlineformset_factory(parent_model=Pathway, model=Stage,
                                    fields=('reaction', 'description'),extra=1,can_delete=True)