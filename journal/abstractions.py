#This file contains abstractions applied all over the project.

from django.db import models

from authorisation.models import StandardUser
from chembook.models import Substance

class AbstractChemicalTransformation(models.Model):
    """Абстрактний клас, який втілює спільні риси моделей синтезу, реакції та бетчу."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    main_product = models.ForeignKey(Substance, on_delete=models.SET_NULL, blank=True, null=True) #TODO: add related_name='...' inheritance somehow
    author = models.ForeignKey(StandardUser, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta: 
        abstract = True
        default_permissions = ('delete','change','view')

    def __str__(self):
        return self.name

