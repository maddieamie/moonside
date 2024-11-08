from django.urls import reverse_lazy
from .models import CustomUser
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

class CustomLoginView(LoginView):
    template_name = 'login.html'

@login_required
def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    
    # Switch profile picture if an image is selected
    if request.GET.get('image'):
        image = request.GET['image']
        if image in ['first_quarter.png', 'full.png', 'new.png', 'waning_crescent.png', 'waning_gibbous.png', 'waxing_crescent.png', 'waxing_gibbous.png']:
            user.profile_picture = f'moon_images/{image}'
            user.save()
    
    return render(request, 'profile.html', {'user': user})

# View to handle updating user profile info
@login_required
def update_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    
    if request.method == 'POST':
        # Assume you're using a form to update user info like location
        user.location = request.POST.get('location')
        user.save()
        return redirect('profile', username=user.username)
    
    return render(request, 'update_profile.html', {'user': user})