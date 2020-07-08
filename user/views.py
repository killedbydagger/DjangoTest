from . import models, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import random
import string
from datetime import datetime

# Create your views here.
@api_view(['POST'])
def getUserLogIn(request):
    body = json.loads(request.body.decode('utf-8'))
    user = models.User.objects.raw('SELECT * FROM user WHERE user_email = %s AND BINARY user_password = %s', [body.get("email"), body.get("password")])
    serializer = serializers.UserSerializer(user, many=True)
    jsonResponse = {
        "data": serializer.data
    }
    if len(serializer.data) == 0:
        jsonResponse.update({"status": "Invalid"})
    else:
        jsonResponse.update({"status": "Success"})
    return Response(jsonResponse)

@api_view(['POST'])
def createNewUser(request):
    body = json.loads(request.body.decode('utf-8'))
    jsonResponse = {
        "data": []
    }
    try:
        models.User.objects.get(user_email=body.get("email"))
        jsonResponse.update({"status": "Email already exist"})
        return Response(jsonResponse)
    except models.User.DoesNotExist:
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        models.User.objects.create(user_email=body.get("email"), user_password=body.get("password"), user_first_name=body.get("first_name"),
                           user_last_name=body.get("last_name"), user_phone=body.get("phone"), user_gender=body.get("gender"),
                           user_dateofbirth=body.get("dateOfBirth"), user_status='Normal', user_activeyn='N',
                           user_token=randomString(15), created_at=formatted_date, updated_at=formatted_date)
        user = models.User.objects.filter(user_email=body.get("email"))
        serializer = serializers.UserSerializer(user, many=True)
        jsonResponse.update({
            "data": serializer.data,
            "status": "Success"
        })
        return Response(jsonResponse)

def randomString(stringLength):
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(stringLength))

@api_view(['GET'])
def registerValidation(request):
    jsonResponse = {
        "data": []
    }
    try:
        user = models.User.objects.get(user_email=request.GET.get('email', ''), user_token=request.GET.get('token', ''))
        user.user_activeyn = 'Y'
        user.user_token = randomString(15)
        user.save()
        jsonResponse.update({"status": "Success"})
        return Response(jsonResponse)
    except models.User.DoesNotExist:
        jsonResponse.update({"status": "Token and Email not match"})
        return Response(jsonResponse)

@api_view(['POST'])
def checkEmailRegister(request):
    body = json.loads(request.body.decode('utf-8'))
    jsonResponse = {
        "data": []
    }
    try:
        models.User.objects.get(user_email=body.get("email"))
        jsonResponse.update({"status": "Exist"})
        return Response(jsonResponse)
    except models.User.DoesNotExist:
        jsonResponse.update({"status": "Not Exist"})
        return Response(jsonResponse)

@api_view(['POST'])
def forgetPassword(request):
    body = json.loads(request.body.decode('utf-8'))
    jsonResponse = {
        "data": []
    }
    try:
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        user = models.User.objects.get(user_email=body.get("email"))
        user.user_password = randomString(10)
        user.user_token = randomString(15)
        user.updated_at = formatted_date
        user.save()
        jsonResponse.update({"status": "Success"})
        return Response(jsonResponse)
    except user.DoesNotExist:
        jsonResponse.update({"status": "Not Exist"})
        return Response(jsonResponse)

@api_view(['POST'])
def changePassword(request):
    body = json.loads(request.body.decode('utf-8'))
    jsonResponse = {
        "data": []
    }
    try:
        user = models.User.objects.get(user_email=body.get("email"))
        if user.user_password == body.get("old_password"):
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            user.user_password = body.get("new_password")
            user.updated_at = formatted_date
            user.save()
            jsonResponse.update({"status": "Success"})
            return Response(jsonResponse)
        else:
            jsonResponse.update({"status": "Invalid"})
            return Response(jsonResponse)
    except user.DoesNotExist:
        jsonResponse.update({"status": "Not Exist"})
        return Response(jsonResponse)

@api_view(['POST'])
def getUserProfile(request):
    body = json.loads(request.body.decode('utf-8'))
    jsonResponse = {
        "data": []
    }
    try:
        user = models.User.objects.get(user_email=body.get("email"))
        serializer = serializers.UserSerializer(user, many=False)
        jsonResponse.update({
            "data": serializer.data,
            "status": "Success"
        })
    except user.DoesNotExist:
        jsonResponse.update({"status": "Not Found"})
        return Response(jsonResponse)