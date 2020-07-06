from django.db import models

# Create your models here.
class Education(models.Model):
    education_id = models.AutoField(primary_key=True)
    education_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'education'