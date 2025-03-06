from django.forms import ModelForm
from .models import Reaction

class ReactionForm(ModelForm):
    class Meta:
        model = Reaction
        fields = [
            'name',
            #'substances',
            'description',
        ]
