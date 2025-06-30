from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('trails/',views.TrailListCreateView.as_view(),name='trail_list'),
    path('trails/<int:pk>/',views.TrailRetreiveView.as_view(),name='trail_detail'),
    path('trail_image/',views.TrailImageListCreateView.as_view(),name='trail_image_list'),
    path('trail_bulk_upload/',views.TrailBulkUploadView.as_view(),name='trail_bulk_upload'),
    path('image_bulk_upload/',views.bulk_upload_trail_images_zip,name='image_bulk_upload'),
]
