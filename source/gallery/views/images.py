from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from gallery.forms import ImagesForm
from gallery.models import Image

import uuid


class ImagesListView(LoginRequiredMixin, ListView):
    model = Image
    context_object_name = 'images'
    template_name = 'gallery_images/index.html'
    ordering = ['-created_at']
    paginate_by = 10
    paginate_orphans = 0

    def get_queryset(self):
        return super(ImagesListView, self).get_queryset().filter(is_private=False)


class ImagesDetailView(LoginRequiredMixin, DetailView):
    model = Image
    context_object_name = 'image'
    template_name = 'gallery_images/detail_view.html'


class ImagesCreateView(LoginRequiredMixin, CreateView):
    model = Image
    form_class = ImagesForm
    template_name = 'gallery_images/create_view.html'

    def get_request_user(self):
        return self.request.user

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ImagesUpdateView(PermissionRequiredMixin, UpdateView):
    model = Image
    template_name = 'gallery_images/update_view.html'
    form_class = ImagesForm
    permission_required = 'gallery.change_image'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author


class ImagesDeleteView(PermissionRequiredMixin, DeleteView):
    model = Image
    context_object_name = 'image'
    template_name = 'gallery_images/delete_view.html'
    success_url = reverse_lazy('gallery:index')
    permission_required = 'gallery.delete_image'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author


class UrlGenerateView(TemplateView):
    template_name = 'gallery_images/detail_view.html'

    def get(self, request, *args, **kwargs):
        image = get_object_or_404(Image, pk=kwargs.get('pk'))
        if image.author == self.request.user:
            image.token = uuid.uuid4()
            image.save()
            return redirect('gallery:token_image', token=image.token)
        return HttpResponseForbidden(content='403 Нет прав доступа')


class ImagesTokenView(TemplateView):
    template_name = 'gallery_images/detail_view.html'

    def get_context_data(self, **kwargs):
        img = get_object_or_404(Image, token=kwargs.get('token'))
        kwargs['image'] = img
        return super().get_context_data(**kwargs)
