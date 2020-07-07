from django.urls import path
from . import views

urlpatterns = [
    path('getUserLogIn', views.getUserLogIn, name="getUserLogIn"),
    path('createNewUser', views.createNewUser, name="createNewUser"),
    path('registerValidation', views.registerValidation, name="registerValidation")
]