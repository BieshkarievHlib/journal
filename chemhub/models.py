from django.db import models

from journal.abstractions import AbstractChemicalTransformation
from chembook.models import Reaction
from authorisation.models import StandardUser

class Project(models.Model):
    name = models.CharField(max_length=255)
    manager = models.ForeignKey(StandardUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='projects')

class Synthesis(AbstractChemicalTransformation):
    number_of_stages = models.IntegerField(default=0)

    class Meta:
        permissions = [
            #('add_reaction', 'Може створювати реакції в цьому синтезі'),   TODO: Визначитися, чи будуть реакції групуватися по синтезах і тільки.
            ('add_pathway','Може додавати шляхи синтезу'),
            ('add_stage','Може додавати стадії синтезу')
        ]

class Pathway(models.Model):
    synthesis = models.ForeignKey(Synthesis, on_delete=models.CASCADE, related_name='pathways')

class Stage(models.Model):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name='stages')
    reaction = models.ForeignKey(Reaction, on_delete=models.SET_NULL, blank=True, null=True, related_name='usages_in_stages')
    
    description = models.CharField(max_length=255, blank=True, null=True)
    order_number = models.PositiveIntegerField(default=0)
    prev_stage = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='next')
    next_stage = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='prev')

    class Meta:
        ordering = ['pathway', 'order_number']