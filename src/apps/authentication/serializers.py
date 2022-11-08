from typing import NoReturn, Optional, OrderedDict

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """User register serializer class"""

    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        """Metaclass with Serializer getting model and included fields"""

        model = User
        fields = ("username", "password", "password_confirm", "email")

    def validate(self, attrs: OrderedDict) -> Optional[OrderedDict]:
        """Validate serializer getting parameters.

        Parameters
        ----------
        attrs : OrderedDict
            RegisterSerializer register create data fields and values

        Returns
        -------
        _ : OrderedDict, optional
            After validation return taking serializer atts
        """

        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data: dict) -> User:
        """Creating a new user instance.

        Parameters
        ----------
        validated_data : dict
            Serializer validated data for creating new user instance

        Returns
        -------
        _: User
            User model instance
        """
        user = User.objects.create_user(username=validated_data["username"], email=validated_data["email"])

        user.set_password(validated_data["password"])
        user.save()

        return user


class SignInTokenSerializer(TokenObtainPairSerializer):
    """Customize SignInTokenSerializer for provide custom token claim"""

    @classmethod
    def get_token(cls, user: User) -> RefreshToken:
        """Add custom token payload

        Parameters
        ----------
        user : User
            User model instance

        Returns
        -------
        _ : RefreshToken
            RefreshToken instance return
        """
        token = super().get_token(user)
        token["username"] = user.username

        return token

    def update(self, instance, validated_data) -> NoReturn:
        raise NotImplementedError("update is not implemented for SignInTokenSerializer")

    def create(self, validated_data) -> NoReturn:
        raise NotImplementedError("create is not implemented for SignInTokenSerializer")
