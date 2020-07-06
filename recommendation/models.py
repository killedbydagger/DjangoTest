from django.db import models

# Create your models here.
class Recommendation(models.Model):
    recom_id = models.IntegerField(primary_key=True)
    user_recom = models.ForeignKey('user.User', models.DO_NOTHING)
    recom_categories = models.CharField(max_length=100)
    recom_location = models.ForeignKey('location.Location', models.DO_NOTHING, db_column='recom_location')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'recommendation'