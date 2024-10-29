from django.urls import path, include
from .views import registerView, profile, update_avatar

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', registerView, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/update_avatar', update_avatar, name='update_avatar'),
]