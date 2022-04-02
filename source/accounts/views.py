from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView

from accounts.forms import MyUserCreationForm
from gallery.models import Image


class RegisterView(CreateView):
    model = User
    template_name = "registration.html"
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('gallery:index')


class ProfileView(DetailView):
    model = get_user_model()
    context_object_name = 'user_obj'
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user == self.get_object():
            context['images'] = self.get_object().images.ordered('-created_at')
            context['albums'] = self.get_object().albums.ordered('-created_at')
        else:
            context['images'] = self.get_object().images.filter(is_private=False)
            context['albums'] = self.get_object().albums.filter(is_private=False)
        print(self.get_object().favorites.all())
        return context
