from rest_framework import serializers
from django.contrib.auth import get_user_model

# Assuming get_user_model() returns your CustomUser model
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'confirmPassword')

    def validate(self, data):
        """
        Check that the two password entries match.
        """
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError({"confirmPassword": "Passwords must match."})
        return data

    def create(self, validated_data):
        """
        Create and return a new user, given the validated data.
        """
        # Remove the confirmPassword field from the validated data.
        validated_data.pop('confirmPassword', None)

        # Use the create_user method to handle user creation.
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user