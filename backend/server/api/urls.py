from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_photo, name='upload_photo'),
    path('process/<int:request_id>/', views.process_personalization, name='process_personalization'),
    path('result/<int:request_id>/', views.get_result, name='get_result'),
    path('requests/', views.list_requests, name='list_requests'),
]
