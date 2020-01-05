from django.db import models


class Fires(models.Model):
    source = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    name = models.CharField(max_length=200, blank=True, null=True)
    size_ac = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    cause = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=65535, decimal_places=65535)
    longitude = models.DecimalField(max_digits=65535, decimal_places=65535)
    state_iso = models.CharField(max_length=10, blank=True, null=True)
    country_iso = models.CharField(max_length=10, blank=True, null=True)
    fire_year = models.IntegerField(blank=True, null=True)
    fire_month = models.IntegerField(blank=True, null=True)
    fire_doy = models.IntegerField(blank=True, null=True)
    size_ha = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fires'