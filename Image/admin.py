from django.contrib import admin

# Register your models here.
from Image.models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'image')


admin.site.register(Image, ImageAdmin)
