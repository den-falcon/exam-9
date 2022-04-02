from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView, CreateView, DetailView

from gallery.forms import AlbumForm
from gallery.models import Album


class AlbumsDetailView(LoginRequiredMixin, DetailView):
    model = Album
    context_object_name = "album"
    template_name = 'gallery_album/detail_view.html'
    search_value = None
    form = None

    def get_context_data(self, **kwargs):
        images = self.object.images.all
        context = super().get_context_data(**kwargs)
        context['images'] = images
        return context


class AlbumsCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'gallery_album/create_view.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AlbumsUpdateView(PermissionRequiredMixin, UpdateView):
    model = Album
    template_name = 'gallery_album/update_view.html'
    form_class = AlbumForm
    permission_required = 'gallery.change_album'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author


class AlbumsDeleteView(PermissionRequiredMixin, DeleteView):
    model = Album
    context_object_name = 'album'
    template_name = 'gallery_album/delete_view.html'
    success_url = reverse_lazy('gallery:index')
    permission_required = 'gallery.delete_album'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author
