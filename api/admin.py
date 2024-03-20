from django.contrib import admin
from .models import TransformerData, TransformerSpecification
# Register your models here.
admin.site.register(TransformerData)
admin.site.register(TransformerSpecification)