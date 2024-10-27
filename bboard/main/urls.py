from django.urls import path

from .models import update_status
from .views import index, create_request, delete_request, add_category, delete_category, manage_categories, \
    update_request_status

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('create_request/', create_request, name='create_request'),
    path('delete_request/<int:pk>/', delete_request, name='delete_request'),
    path('update_status/<int:pk>/<str:status>/', update_status, name='update_status'),
    path('add_category/', add_category, name='add_category'),
    path('delete_category/<int:pk>/', delete_category, name='delete_category'),
    path('manage_categories/', manage_categories, name='manage_categories'),
    path('update_request_status/<int:pk>/', update_request_status, name='update_request_status')
]