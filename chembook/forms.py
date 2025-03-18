from django.forms import ModelForm, CharField, inlineformset_factory
from .models import Reaction, Substance, Batch, BatchSubstance

from guardian.shortcuts import assign_perm

class ReactionForm(ModelForm):
    class Meta:
        model = Reaction
        fields = [
            'name',
            'description',
        ]

    substances_input = CharField(required=False,
                                 help_text='Введіть речовини через кому')

    def __init__(self, *args, user = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
    def save(self, commit=True):
        reaction = super().save(commit=False)

        substances_text = self.cleaned_data.get('substances_input') #Обробляємо інформацію про substances
        if substances_text:
            names = [name.strip() for name in substances_text.split(',')]
            substances = [Substance.objects.get_or_create(name=name)[0] for name in names]
            
            reaction.save()               
            reaction.substances.set(substances)
        
        if not reaction.author and self.user: #Зберігаємо автора та надаємо йому дозволи при створенні нової або апдейті нічийної реакції
            reaction.save()
            reaction.author = self.user

            assign_perm('add_batch', reaction.author, reaction)
            assign_perm('view_reaction', reaction.author, reaction)      
            assign_perm('delete_reaction', reaction.author, reaction)   
            assign_perm('change_reaction', reaction.author, reaction)   
            

        if commit:
            reaction.save()
        
        return reaction
    
class BatchForm(ModelForm):                                             #TODO: розглянути наслідування від ReactionForm
                                                                        #TODO: прикрутити повноцінний функціонал для апдейту
    class Meta:
        model = Batch
        fields = [
            'name',
            'description',
        ]
    
    def __init__(self, *args, user = None, reaction = None, **kwargs):
        self.user = user
        self.reaction = Reaction.objects.get(pk=reaction)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        batch = super().save(commit=False)
        batch.reaction =  self.reaction
        batch.save()

        #batch.substances.set([BatchSubstance.objects.get_or_create(batch=self.instance, substance=substance)[0]
        #                  for substance in self.reaction.substances.all()])
        
        if not batch.author and self.user: #Зберігаємо автора та надаємо йому дозволи при створенні нової або апдейті нічийного бетчу
            batch.save()
            batch.author = self.user

            assign_perm('view_batch', batch.author, batch)      
            assign_perm('delete_batch', batch.author, batch)   
            assign_perm('change_batch', batch.author, batch)

        if commit:
            batch.save()

        return batch

BatchSubstanceFormSet = inlineformset_factory(parent_model=Batch,model=BatchSubstance,
                                              fields=('substance', 'mass'),extra=1,can_delete=True)