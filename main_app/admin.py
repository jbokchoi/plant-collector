from django.contrib import admin
from .models import Plant, Feeding, Accessory, Photo

# Register your models here.
admin.site.register(Plant)
admin.site.register(Feeding)
admin.site.register(Accessory)
admin.site.register(Photo)