from rest_framework import serializers
from .models import PrintOrder
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']  # ✅ Include username & email

class PrintOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # ✅ Nest user details inside order

    class Meta:
        model = PrintOrder
        fields = '__all__'
