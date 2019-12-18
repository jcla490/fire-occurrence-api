from rest_framework import serializers
from fireapi.models import Fires
from django_filters.rest_framework import DjangoFilterBackend


class FiresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fires
        fields = ['id', 'source', 'country', 'name', 'size_ac', 'start_date', 'end_date', 'cause', 'state', 'latitude', 'longitude']
        
        extra_kwargs = {
            'size_ac': {'max_digits': 16, 'decimal_places': 2},
            'latitude': {'max_digits': 16, 'decimal_places': 6},
            'longitude': {'max_digits': 16, 'decimal_places': 6},
        }

