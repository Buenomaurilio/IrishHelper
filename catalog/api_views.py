from rest_framework import generics
from django.utils import timezone
from .models import Resource
from .serializers import ResourceSerializer

class ResourceList(generics.ListAPIView):
    serializer_class = ResourceSerializer

    def get_queryset(self):
        qs = Resource.objects.filter(is_active=True).order_by("section","sort_order","id")
        section = self.request.query_params.get("section")
        locale  = self.request.query_params.get("locale")
        country = self.request.query_params.get("country")
        search  = self.request.query_params.get("q")

        if section: qs = qs.filter(section=section)
        if locale:  qs = qs.filter(locale=locale)
        if country: qs = qs.filter(country__in=["", country])
        if search:
            qs = qs.filter(title__icontains=search) | qs.filter(description__icontains=search)
        return qs
