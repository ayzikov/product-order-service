# base
# installed
from rest_framework import serializers
# local
from apps.orderserviceapi import models


# PROVIDER
class ProviderOutputDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        exclude = ["id"]


class ProviderOutputListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = "__all__"


class ProviderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = "__all__"


class ProviderModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        exclude = ["id"]


# BUYER
class BuyerOutputDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Buyer
        fields = ["id", "username", "first_name", "last_name", "age", "email"]


class BuyerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Buyer
        exclude = ["groups", "user_permissions"]