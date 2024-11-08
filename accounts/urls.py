from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import SignUpView, profile_view, update_profile, CustomLoginView

urlpatterns = [
    
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('update-profile/<str:username>/', update_profile, name='update_profile')
    
]
