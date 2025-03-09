from django.forms import ModelForm, CharField
from .models import Reaction, Substance
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

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
        
        if not reaction.author and self.user:
            reaction.save()
            reaction.author = self.user                                 #Зберігаємо автора
                                                                        #Видаємо автору базові дозволи, тільки якщо авторa немає      
            content_type = ContentType.objects.get_for_model(Reaction)
            permissions = Permission.objects.filter(content_type=content_type,codename__in=['change_reaction', 'delete_reaction', 'view_reaction',
                                                                                            'add_reaction'])
            reaction.author.user_permissions.add(*permissions)

        if commit:
            reaction.save()
        
        return reaction