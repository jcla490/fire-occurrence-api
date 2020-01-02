from rest_framework import serializers
from fireapi.models import Fires
from django_filters.rest_framework import DjangoFilterBackend


class FiresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fires
        fields = ['id', 'country', 'country_iso', 'name', 'size_ac', 'size_ha','start_date', 'end_date', 'cause', 'state', 'state_iso','latitude', 'longitude', 'fire_year', 'fire_month', 'fire_doy']
        
        extra_kwargs = {
            'size_ac': {'max_digits': 16, 'decimal_places': 6},
            'size_ha': {'max_digits': 16, 'decimal_places': 6},
            'latitude': {'max_digits': 16, 'decimal_places': 6},
            'longitude': {'max_digits': 16, 'decimal_places': 6},
        }

