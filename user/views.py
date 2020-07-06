from . import models, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import random
import string
from datetime import datetime
from django.db import connection

# Create your views here.
@api_view(['POST'])
def getUserLogIn(request):
    body = json.loads(request.body.decode('utf-8'))
    user = models.User.objects.raw('SELECT * FROM user WHERE user_email = %s AND BINARY user_password = %s', [body.get("email"), body.get("password")])
    serializer = serializers.UserSerializer(user, many=True)
    if len(serializer.data) == 0:
        jsonResponse = {
            "data": serializer.data,
            "status": "Invalid"
        }
    else:
        jsonResponse = {
            "data": serializer.data,
            "status": "Success"
        }
    return Response(jsonResponse)

@api_view(['POST'])
def createNewUser(request):
    body = json.loads(request.body.decode('utf-8'))
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(user_id) FROM `user` WHERE user_email = %s", [body.get("email")])
        result = cursor.fetchone()
    if result[0] == 0:
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        with connection.cursor() as cursor:
            cursor.execute('''INSERT INTO `user`
                                (user_email, user_password, user_first_name,
                                user_last_name, user_phone, user_gender,
                                user_dateOfBirth, user_status, user_activeYN, user_token, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                               [body.get("email"), body.get("password"), body.get("first_name"),
                                body.get("last_name"), body.get("phone"), body.get("gender"),
                                body.get("dateOfBirth"), 'Normal', 'N',
                                randomString(15), formatted_date, formatted_date])
        user = models.User.objects.raw('SELECT * FROM user WHERE user_email = %s', [body.get("email")])
        serializer = serializers.UserSerializer(user, many=True)
        jsonResponse = {
            "data": serializer.data,
            "status": "Success"
        }
        return Response(jsonResponse)
    else:
        jsonResponse = {
            "data": [],
            "status": "Email already exist"
        }
    return Response(jsonResponse)

def randomString(stringLength):
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(stringLength))

