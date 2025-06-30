from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json,csv,io
from django.db import transaction
import zipfile
import pandas as pd
from io import BytesIO
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
# Create your views here.

class TrailListCreateView(generics.ListCreateAPIView):
    queryset= Trail.objects.all()
    serializer_class = TrailSerializer

class TrailImageListCreateView(generics.ListCreateAPIView):
    queryset = TrailImage.objects.all()
    serializer_class = TrailImageSerializer

class TrailRetreiveView(generics.RetrieveUpdateAPIView):
    queryset = Trail.objects.all()
    serializer_class = TrailSerializer
    lookup_field = 'pk'

class TrailBulkUploadView(APIView):
    def post(self, request):
        json_file = request.FILES.get('file')

        if not json_file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = json.load(json_file)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON file'}, status=status.HTTP_400_BAD_REQUEST)

        for trail in data:
            Trail.objects.update_or_create(
                name=trail['name'],
                defaults={
                    'region': trail['region'],
                    'description': trail['description'],
                    'distance_km': trail['distance_m'] / 1000,
                    'duration_days': trail['duration_days'],
                    'elevation': trail['elevation'],
                    'difficulty': trail['difficulty'],
                    'start_lat': trail['start_point']['lat'],
                    'start_lng': trail['start_point']['lng'],
                    'end_lat': trail['end_point']['lat'],
                    'end_lng': trail['end_point']['lng'],
                }
            )

        return Response({'message': 'Trails uploaded successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def bulk_upload_trail_images_zip(request):
    zip_file = request.FILES.get('file')

    if not zip_file or not zip_file.name.endswith('.zip'):
        return Response({'error': 'Only .zip files are allowed'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with zipfile.ZipFile(zip_file) as zf:
            file_names = zf.namelist()

            if 'newest.csv' not in file_names:
                return Response({'error': 'CSV file "trail_images.csv" not found in ZIP'}, status=400)

            # Read CSV file from ZIP
            csv_file = zf.open('newest.csv')
            df = pd.read_csv(csv_file)

            created_count = 0
            failed_uploads = []

            with transaction.atomic():
                for _, row in df.iterrows():
                    trail_id = row.get('trail_id')
                    image_filename = row.get('image_file')

                    if pd.isna(trail_id) or pd.isna(image_filename):
                        failed_uploads.append(f"Missing data in row: {row.to_dict()}")
                        continue

                    try:
                        trail = Trail.objects.get(id=int(trail_id))
                    except Trail.DoesNotExist:
                        failed_uploads.append(f"Trail with ID {trail_id} not found.")
                        continue

                    if image_filename not in file_names:
                        failed_uploads.append(f"Image file '{image_filename}' not found in ZIP.")
                        continue

                    image_file = zf.open(image_filename)
                    trail_image = TrailImage(trail=trail)
                    trail_image.image.save(image_filename, ContentFile(image_file.read()), save=True)
                    created_count += 1

    except zipfile.BadZipFile:
        return Response({'error': 'Uploaded file is not a valid ZIP file.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        'message': f"{created_count} trail images uploaded.",
        'failed_uploads': failed_uploads
    }, status=status.HTTP_207_MULTI_STATUS if failed_uploads else status.HTTP_201_CREATED)