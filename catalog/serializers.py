from rest_framework import serializers
from .models import Resource

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ["id","section","title","description","url","phone","address","is_official","country","locale","sort_order","is_active","updated_at","created_at"]
