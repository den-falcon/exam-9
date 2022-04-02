from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from gallery.models import Album, Image


class ImagesFavoriteView(TemplateView):

    def post(self, request, *args, **kwargs):
        image = get_object_or_404(Image, pk=self.kwargs.get('pk'))
        image.add_favorite()
        print('favorite')
        return JsonResponse(image.make_response())

    def delete(self, request, *args, **kwargs):
        image = get_object_or_404(Image, pk=self.kwargs.get('pk'))
        image.delete_favorite()
        return JsonResponse(image.make_response())


class AlbumsFavoriteView(TemplateView):

    def post(self, request, *args, **kwargs):
        album = get_object_or_404(Album, pk=self.kwargs.get('pk'))
        album.add_favorite()
        print('favorite')
        return JsonResponse(album.make_response())

    def delete(self, request, *args, **kwargs):
        album = get_object_or_404(Album, pk=self.kwargs.get('pk'))
        album.delete_favorite()
        return JsonResponse(album.make_response())
