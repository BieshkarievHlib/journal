from django.db import models

# Create your models here.

class Substance(models.Model):
    name = models.CharField(max_length=255)
    smiles = models.CharField(max_length=255,blank=True, null=True)
    image = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.name

class Reaction(models.Model):
    name = models.CharField(max_length=255)
    substances = models.ManyToManyField(Substance, blank=True, null=True)
    description = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return self.name