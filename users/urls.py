from django.urls import path
from .views import *



urlpatterns = [
    path('auht/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileView.as_view(), name='profile-update'),
    path('logout/', LogoutView.as_view(), name='logout'),
]


