from rest_framework import serializers
from .models import *

class TrailImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrailImage
        fields = ['id','trail','image']

class TrailSerializer(serializers.ModelSerializer):
    start_point = serializers.SerializerMethodField()
    end_point = serializers.SerializerMethodField()
    images = TrailImageSerializer(many=True, read_only=True)

    class Meta:
        model = Trail
        fields = [
            'id', 'name','description', 'region', 'distance_km', 'duration_days',
            'elevation', 'difficulty', 'start_point',
            'end_point','images'
        ]

    def get_start_point(self, obj):
        return {"lat": obj.start_lat, "lng": obj.start_lng}

    def get_end_point(self, obj):
        return {"lat": obj.end_lat, "lng": obj.end_lng}