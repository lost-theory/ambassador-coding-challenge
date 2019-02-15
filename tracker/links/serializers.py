from rest_framework import serializers

from .models import Link

class LinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Link
        fields = ('title', 'url', 'creation_date', 'last_modified_date')
