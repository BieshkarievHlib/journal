from django.db import models
from authorisation.models import StandardUser

# Create your models here.

class Substance(models.Model):
    name = models.CharField(max_length=255)
    smiles = models.CharField(max_length=255,blank=True, null=True)
    image = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.name

class Reaction(models.Model):
    name = models.CharField(max_length=255)
    substances = models.ManyToManyField(Substance, blank=True)
    description = models.CharField(max_length=255,blank=True, null=True)
    author = models.ForeignKey(StandardUser, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        default_permissions = ('add','delete','change','view')
        permissions = [

        ]

    def __str__(self):
        return self.name