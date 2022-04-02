from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django_currentuser.middleware import get_current_authenticated_user


class Favorites(models.Model):
    user = models.ForeignKey(get_user_model(),
                             related_name='favorites',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Album(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название', )
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание', )
    author = models.ForeignKey(get_user_model(), related_name='albums', on_delete=models.CASCADE,
                               verbose_name='Автор', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', )
    is_private = models.BooleanField(default=False, verbose_name='Приватноcть', )
    favorites = GenericRelation(Favorites)

    def get_object_type(self):
        return ContentType.objects.get_for_model(self)

    def add_favorite(self):
        obj_type = self.get_object_type()
        Favorites.objects.get_or_create(
            content_type=obj_type, object_id=self.id, user=get_current_authenticated_user())

    def delete_favorite(self):
        obj_type = self.get_object_type()
        Favorites.objects.filter(
            content_type=obj_type, object_id=self.id, user=get_current_authenticated_user()
        ).delete()

    def is_favorites(self):
        user = get_current_authenticated_user()
        if not user:
            return False
        obj_type = ContentType.objects.get_for_model(self)
        favorites = Favorites.objects.filter(
            content_type=obj_type, object_id=self.id, user=user).exists()
        return favorites

    def make_response(self):
        response = {
            'is_fan': self.is_favorites()
        }
        return response

    def get_absolute_url(self):
        return reverse('gallery:albums_detail_view', kwargs={'pk': self.pk})


class Image(models.Model):
    img = models.ImageField(verbose_name='Фото', upload_to='gallery_images/', )
    caption = models.TextField(max_length=500, verbose_name='Подпись', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', )
    author = models.ForeignKey(get_user_model(), related_name='images', on_delete=models.CASCADE,
                               verbose_name='Автор', )
    is_private = models.BooleanField(default=False, verbose_name='Приватноcть', )
    album = models.ForeignKey(Album, null=True, blank=True, related_name='images', on_delete=models.CASCADE,
                              verbose_name='Альбом', )
    token = models.CharField(max_length=100, null=True, blank=True, verbose_name='Уникальный токен', )
    favorites = GenericRelation(Favorites)

    def get_object_type(self):
        return ContentType.objects.get_for_model(self)

    def add_favorite(self):
        obj_type = self.get_object_type()
        Favorites.objects.get_or_create(
            content_type=obj_type, object_id=self.id, user=get_current_authenticated_user())

    def delete_favorite(self):
        obj_type = self.get_object_type()
        Favorites.objects.filter(
            content_type=obj_type, object_id=self.id, user=get_current_authenticated_user()
        ).delete()

    def is_favorites(self):
        user = get_current_authenticated_user()
        if not user:
            return False
        obj_type = ContentType.objects.get_for_model(self)
        favorites = Favorites.objects.filter(
            content_type=obj_type, object_id=self.id, user=user).exists()
        return favorites

    def make_response(self):
        response = {
            'is_fan': self.is_favorites()
        }
        return response

    def get_absolute_url(self):
        return reverse('gallery:images_detail_view', kwargs={'pk': self.pk})
