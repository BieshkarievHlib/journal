from django.db import models
from authorisation.models import StandardUser

# Create your models here.

class Substance(models.Model):
    name = models.CharField(max_length=255)
    smiles = models.CharField(max_length=255,blank=True, null=True)
    image = models.FileField(blank=True, null=True)
    molecular_mass = models.FloatField(default=0, blank=True, null=True) #TODO: прибрати бленк і нулл, прописати логіку для дефолту і вайпнути БД

    def __str__(self):
        return self.name

class Reaction(models.Model):
    name = models.CharField(max_length=255)
    substances = models.ManyToManyField(Substance, blank=True)
    description = models.CharField(max_length=255,blank=True, null=True)
    author = models.ForeignKey(StandardUser, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        default_permissions = ('add','delete','change','view')
        permissions = [

        ]

    def __str__(self):
        return self.name

class Batch(models.Model):                      #TODO: розглянути можливість наслідування від Reaction, якщо переписати Reaction або написати спільний батьківський клас
    """
    ACHTUNG! 
    Batch створювати ВИКЛЮЧНО через форму: reaction та batch.substances присвоюється тільки в BatchForm.save()
    """
    reaction = models.ForeignKey(Reaction, on_delete=models.CASCADE, related_name='batches')
    description = models.CharField(max_length=255,blank=True, null=True)
    sample_number  = models.IntegerField(default=0)      #TODO: прописати дефолт через інкремент += 1 при створенні, декремент -= 1 при видаленні. Або замінити на шось реально корисне
    is_probe = models.BooleanField(default=False)
    author = models.ForeignKey(StandardUser, on_delete=models.SET_NULL, blank=True, null=True)

class BatchSubstance(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='substances')
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE, related_name='usages_in_batches')

    quantity = models.FloatField(default=0)
    equivalents = models.FloatField(default=0)
    mass = models.FloatField(default=0)