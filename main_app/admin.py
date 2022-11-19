from django.contrib import admin
from .models import Album, Listen, List, Photo

# Register your models here.
admin.site.register(Album)
admin.site.register(Listen)
admin.site.register(List)
admin.site.register(Photo)