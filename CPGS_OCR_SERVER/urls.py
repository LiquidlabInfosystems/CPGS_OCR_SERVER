from django.urls import path

from app import views
# from . import views  # Assuming the views are in the same directory

urlpatterns = [
    # path('admin/', views.server_status, name='server_status'),
    path('', views.get_ocr, name='getocr'),
]