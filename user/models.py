from django.db import models
from datetime import datetime

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.CharField(unique=True, max_length=50)
    user_password = models.CharField(max_length=25)
    user_first_name = models.CharField(max_length=100)
    user_last_name = models.CharField(max_length=100, blank=True, null=True)
    user_phone = models.CharField(max_length=15)
    user_gender = models.CharField(max_length=10)
    user_dateofbirth = models.DateTimeField(db_column='user_dateOfBirth')  # Field name made lowercase.
    user_cv = models.CharField(max_length=255, blank=True, null=True)
    user_lasteducation = models.ForeignKey('education.Education', models.DO_NOTHING, db_column='user_lastEducation', blank=True, null=True)  # Field name made lowercase.
    user_location = models.ForeignKey('location.Location', models.DO_NOTHING, db_column='user_location', blank=True, null=True)
    user_description = models.CharField(max_length=255, blank=True, null=True)
    user_status = models.CharField(max_length=10)
    user_recommendation = models.ForeignKey('recommendation.Recommendation', models.DO_NOTHING, db_column='recommendation', blank=True, null=True)
    user_activeyn = models.CharField(db_column='user_activeYN', max_length=1)  # Field name made lowercase.
    user_token = models.CharField(max_length=20)
    firebase_token_notification = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user'
