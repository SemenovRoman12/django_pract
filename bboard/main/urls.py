from django.urls import path
from .views import index, create_request, delete_request

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('create_request/', create_request, name='create_request'),
    path('delete_request/<int:pk>/', delete_request, name='delete_request'),
]