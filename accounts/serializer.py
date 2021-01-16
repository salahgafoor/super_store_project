from rest_framework import serializers
from accounts import models

class HelloSerializer(serializers.Serializer):
    """Serializers a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    class Meta:
        model = models.UserProfileInfo
        fields = ('id','email','name','password')
        extra_kwargs = {
            'password':{
                'write_only':True,
                'style':{'input_type':'password'}
            }
        }

    def create(self,validated_data):
        """Create and return a new user"""
        user = models.UserProfileInfo.objects.create_user(
            email = validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = [
            "id",
            "name",
            "description",
            "image",
            "price",
        ]

    def get_image(self, obj):
        try:
            return obj.productimage_set.first().image.url
        except:
            return None

class ProductDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = models.Product
        fields = [
            "id",
            "name",
            "description",
            "image",
            "price",
        ]

    def get_image(self, obj):
        return obj.productimage_set.first().image.url            
        
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = [
            "id",
            "name",
            "description",
            "image",
            "price",
        ]

class OrderDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='userprofileinfo.name')
    class Meta:
        model = models.Order
        fields = [
            "name",
            "product",
            "total_amount",
        ]
                 