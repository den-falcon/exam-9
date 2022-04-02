from django import forms

from gallery.models import Image, Album

from django_currentuser.middleware import get_current_authenticated_user


class ImagesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImagesForm, self).__init__(*args, **kwargs)
        self.fields['album'].queryset = Album.objects.filter(author=get_current_authenticated_user())

    class Meta:
        model = Image
        exclude = ['author', 'token']


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        exclude = ['author']
