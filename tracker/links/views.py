from rest_framework import viewsets
from .serializers import LinkSerializer

from .models import Link

class LinkViewSet(viewsets.ModelViewSet):
    """
    REST API endpoint for links.
    """
    queryset = Link.objects.all().order_by('-creation_date')
    serializer_class = LinkSerializer
