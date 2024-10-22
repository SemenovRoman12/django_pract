from django.urls import path, include
from .views import registerView, profile

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', registerView, name='register'),
    path('profile/', profile, name='profile'),
]