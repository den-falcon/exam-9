from django.contrib import admin

from gallery.models import Album, Image

admin.site.register(Image)
admin.site.register(Album)
