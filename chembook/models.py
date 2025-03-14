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

class Synthesis(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    main_product = models.ForeignKey(Substance, on_delete=models.SET_NULL, blank=True, null=True, related_name='producing_syntheses')
    author = models.ForeignKey(StandardUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='syntheses')
    number_of_stages = models.IntegerField(default=0)
#TODO:manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, blank=True, null=True, related_name='syntheses')

    class Meta:
        default_permissions = ('delete','change','view')
        permissions = [
            #('add_reaction', 'Може створювати реакції в цьому синтезі'),   TODO: Визначитися, чи будуть реакції групуватися по синтезах і тільки.
            ('add_pathway','Може додавати шляхи синтезу'),
            ('add_stage','Може додавати стадії синтезу')
        ]

    def __str__(self):
        return self.name

class Reaction(models.Model):
    name = models.CharField(max_length=255)
    substances = models.ManyToManyField(Substance, blank=True)
    description = models.CharField(max_length=255,blank=True, null=True)
    author = models.ForeignKey(StandardUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='owned_reactions', db_index=True)
    main_product = models.ForeignKey(Substance, on_delete=models.SET_NULL, blank=True, null=True, related_name='producing_reactions')

    class Meta:
        default_permissions = ('delete','change','view')
        permissions = [
            ('add_batch', 'Може створювати бетчі для цієї реакції')
        ]

    def __str__(self):
        return self.name

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

    class Meta:
        default_permissions = ('add','delete','change','view')
        permissions = [

        ]

class BatchSubstance(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='substances')
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE, related_name='usages_in_batches')

    quantity = models.FloatField(default=0)
    equivalents = models.FloatField(default=0)
    mass = models.FloatField(default=0)