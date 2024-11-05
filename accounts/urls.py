from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import SignUpView, ProfileView, CustomLoginView

urlpatterns = [
    
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile')
    
]
