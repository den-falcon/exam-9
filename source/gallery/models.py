from django.contrib.auth import get_user_model
from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название', )
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание', )
    author = models.ForeignKey(get_user_model(), related_name='albums', on_delete=models.CASCADE,
                               verbose_name='Автор', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', )
    is_private = models.BooleanField(default=False, verbose_name='Приватноcть', )


class Image(models.Model):
    img = models.ImageField(verbose_name='Фото', upload_to='images/', )
    caption = models.TextField(max_length=500, verbose_name='Подпись', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', )
    author = models.ForeignKey(get_user_model(), related_name='images', on_delete=models.CASCADE,
                               verbose_name='Автор', )
    is_private = models.BooleanField(default=False, verbose_name='Приватноcть', )
    album = models.ForeignKey(Album, null=True, blank=True, related_name='images', on_delete=models.CASCADE,
                              verbose_name='Альбом', )
