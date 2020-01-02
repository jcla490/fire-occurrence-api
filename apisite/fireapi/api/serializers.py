from rest_framework import serializers
from fireapi.models import Fires
from django_filters.rest_framework import DjangoFilterBackend


class FiresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fires
        fields = ['id', 'country', 'country_iso', 'state', 'state_iso', 'latitude', 'longitude', 'start_date', 'end_date', 'fire_year', 'fire_month', 'fire_doy', 'name', 'size_ac', 'size_ha', 'cause']
        
        extra_kwargs = {
            'size_ac': {'max_digits': 16, 'decimal_places': 6},
            'size_ha': {'max_digits': 16, 'decimal_places': 6},
            'latitude': {'max_digits': 16, 'decimal_places': 6},
            'longitude': {'max_digits': 16, 'decimal_places': 6},
        }

