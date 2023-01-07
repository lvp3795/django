from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import authentication_classes, permission_classes
from .models import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        """
        Hàm create dùng để tạo một đối tượng mới từ dữ liệu đã được xác thực.

        Input:
            validated_data (dict): Dữ liệu đã được xác thực.

        Output:
            instance: Đối tượng đã được tạo từ dữ liệu xác thực.
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        Hàm update dùng để cập nhật thông tin của một đối tượng đã tồn tại.

        Input:
            instance: Đối tượng cần cập nhật.
            validated_data (dict): Dữ liệu mới đã được xác thực.

        Output:
            instance: Đối tượng đã được cập nhật từ dữ liệu xác thực.
        """
        for attr, value in validated_data.items():
            if (attr == 'password'):
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('name', 'email', 'password', 'phone', 'gender',
                  'is_active', 'is_staff', 'is_superuser')
