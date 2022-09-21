from rest_framework import serializers
from rest_framework.authtoken.admin import User

from items.models import Items


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['id', 'name', 'location', 'isPrivate', 'price', 'owner', 'borrowed_location']


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['id', 'borrowed_location', 'borrower', 'isBorrowed']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class UserItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    def create(self, validated_data):
        user_dict = validated_data.pop('owner')
        user_obj, created = User.objects.get_or_create(**user_dict)
        return Items.objects.create(user=user_obj, **validated_data)

    class Meta:
        model = Items
        fields = ['id', 'name', 'location', 'isPrivate', 'price', 'isBorrowed', 'owner', 'borrowed_location']
