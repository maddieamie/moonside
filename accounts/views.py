from django.urls import reverse_lazy
from .models import CustomUser
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView

from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

class CustomLoginView(LoginView):
    template_name = 'login.html'

class ProfileView(DetailView):
    model = CustomUser
    template_name = 'profile.html'  # Template for displaying user profile
    context_object_name = 'user_profile'