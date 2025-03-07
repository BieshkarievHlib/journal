from django.forms import ModelForm, CharField
from .models import Reaction, Substance

class ReactionForm(ModelForm):
    class Meta:
        model = Reaction
        fields = [
            'name',
            'description',
        ]

    substances_input = CharField(required=False,
                                 help_text='Введіть речовини через кому')

    def save(self, commit=True):
        reaction = super().save(commit=False) 
        substances_text = self.cleaned_data.get('substances_input')

        if substances_text:
            names = [name.strip() for name in substances_text.split(',')]
            print(f'Names here: {names}')
            substances = [Substance.objects.get_or_create(name=name)[0] for name in names]
            
            reaction.save()                     
            reaction.substances.set(substances)
        
        if commit:
            reaction.save()
        
        return reaction