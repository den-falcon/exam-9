from django.urls import path

from gallery.views.album import AlbumsDetailView, AlbumsCreateView, AlbumsUpdateView, AlbumsDeleteView
from gallery.views.favorites import ImagesFavoriteView, AlbumsFavoriteView
from gallery.views.images import ImagesListView, ImagesDetailView, ImagesCreateView, ImagesUpdateView, ImagesDeleteView, \
    ImagesTokenView, UrlGenerateView

app_name = 'gallery'

urlpatterns = [
    path('', ImagesListView.as_view(), name='index'),
    path('images/add/', ImagesCreateView.as_view(), name='images_create_view'),
    path('images/<int:pk>', ImagesDetailView.as_view(), name='images_detail_view'),
    path('images/<int:pk>/update/', ImagesUpdateView.as_view(), name='images_update_view'),
    path('images/<int:pk>/delete/', ImagesDeleteView.as_view(), name='images_delete_view'),
    path('albums/add/', AlbumsCreateView.as_view(), name='albums_create_view'),
    path('albums/<int:pk>', AlbumsDetailView.as_view(), name='albums_detail_view'),
    path('albums/<int:pk>/update/', AlbumsUpdateView.as_view(), name='albums_update_view'),
    path('albums/<int:pk>/delete/', AlbumsDeleteView.as_view(), name='albums_delete_view'),
    path('images/<token>/', ImagesTokenView.as_view(), name='token_image'),
    path('images/<int:pk>/generate_url/', UrlGenerateView.as_view(), name='token_image_generate'),
    path('images/<int:pk>/favorite', ImagesFavoriteView.as_view(), name='image_favorite'),
    path('albums/<int:pk>/favorite', AlbumsFavoriteView.as_view(), name='album_favorite'),
]
