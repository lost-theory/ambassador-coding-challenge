from rest_framework import serializers

from .models import Link

class LinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Link
        fields = ('title', 'url', 'creation_date', 'last_modified_date')

    def to_representation(self, obj):
        out = super().to_representation(obj)
        if hasattr(obj, 'clicks'):
            out['clicks'] = obj.clicks
        return out
