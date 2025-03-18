from django.contrib import admin

from .models import Synthesis, Pathway, Stage

admin.site.register(Synthesis)
admin.site.register(Pathway)
admin.site.register(Stage)
