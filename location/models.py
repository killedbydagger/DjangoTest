from django.db import models

# Create your models here.
class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'location'