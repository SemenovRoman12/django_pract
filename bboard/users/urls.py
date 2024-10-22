from django.urls import path, include
from .views import registerView

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', registerView, name='register'),
]