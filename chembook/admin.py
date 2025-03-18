from django.contrib import admin
from .models import Reaction, Substance, Batch

admin.site.register(Reaction)
admin.site.register(Substance)
admin.site.register(Batch)
