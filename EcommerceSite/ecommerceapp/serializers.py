from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Items, productsUserReviewModel


# Customer Registration Serializer
class accountsCustomerCreationSerializer(serializers.ModelSerializer):

    def validate(self, data):
        email = data.get("email", None)
        queryset = get_user_model().objects.filter(email=email)
        if queryset.exists():
            raise serializers.ValidationError(
                {"error": "Usr already exists with this email.", 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return data

    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password']

    def create(self, validated_data):
        name = validated_data.pop('name')
        user_instance = get_user_model().objects.create_customer(**validated_data)
        user_instance.name = name
        user_instance.save()
        return user_instance


# Seller Registration Serializer
class accountsSellerCreationSerializer(serializers.ModelSerializer):

    def validate(self, data):
        email = data.get("email", None)
        queryset = get_user_model().objects.filter(email=email)
        if queryset.exists():
            raise serializers.ValidationError(
                {"error": "Usr already exists with this email.", 'status': status.HTTP_400_BAD_REQUEST})
        else:
            return data

    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password']

    def create(self, validated_data):
        name = validated_data.pop('name')
        user_instance = get_user_model().objects.create_seller(**validated_data)
        user_instance.name = name
        user_instance.save()
        return user_instance


# User LogIn Serializer
class accountEmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=100, required=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        try:
            user = get_user_model().objects.get(email=email, is_active=True)
            if not user.check_password(password):
                raise serializers.ValidationError(
                    {"password": "Invalid Password.", 'status': status.HTTP_400_BAD_REQUEST})

        except get_user_model().DoesNotExist:
            raise serializers.ValidationError(
                {"email": "A user with this email doesn't exists", 'status': status.HTTP_400_BAD_REQUEST})
        return data

    class Meta:
        fields = '__all__'

    def to_representation(self, instance):
        instance.pop('password')
        user = get_user_model().objects.get(email=instance['email'])
        jwt_token = RefreshToken.for_user(user)
        instance["access_token"] = str(jwt_token.access_token),
        instance["refresh_token"] = str(jwt_token)
        instance['name'] = user.name
        instance['is_customer'] = user.is_customer
        instance['is_seller'] = user.is_seller
        return instance
        return ({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        })
class productserializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = "__all__"
class reviewserializer(serializers.Serializer):
    productdetails = serializers.SerializerMethodField()
    def get_productdetails(self,id):
        obj=Items.objects.all()
        products = productserializer(obj)
        return products.data
    class Meta:
        model = productsUserReviewModel
        fields="__all__"
