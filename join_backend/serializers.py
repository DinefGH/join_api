from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Contact
from .models import Category
from .models import Subtask
from .models import Task



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
    
    
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')  # Specify the fields you want to include
        read_only_fields = ('id', 'name', 'email')


class ContactSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Contact
        fields = ('id', 'user', 'name', 'email', 'phone', 'color')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color']


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'text', 'completed']

class TaskSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=True,
        required=False
    )
    assigned_to = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Contact.objects.all(),
        required=False
    )
    subtasks = SubtaskSerializer(many=True, required=False)
    creator = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'due_date', 'category', 'assigned_to', 'creator', 'subtasks', 'status']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['creator'] = request.user

        subtasks_data = validated_data.pop('subtasks', [])
        assigned_to_data = validated_data.pop('assigned_to', [])
        task = Task.objects.create(**validated_data)
        task.assigned_to.set(assigned_to_data)

        for subtask_data in subtasks_data:
            subtask = Subtask.objects.create(**subtask_data)
            task.subtasks.add(subtask)

        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        assigned_to_data = validated_data.pop('assigned_to', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.assigned_to.set(assigned_to_data)

        current_subtasks = {subtask.id: subtask for subtask in instance.subtasks.all()}
        updated_subtasks = []

        for subtask_data in subtasks_data:
            subtask_id = subtask_data.get('id')
            if subtask_id and subtask_id in current_subtasks:
                subtask = current_subtasks.pop(subtask_id)
                for key, value in subtask_data.items():
                    setattr(subtask, key, value)
                subtask.save()
                updated_subtasks.append(subtask)
            else:
                new_subtask = Subtask.objects.create(**subtask_data)
                updated_subtasks.append(new_subtask)

        for subtask in current_subtasks.values():
            instance.subtasks.remove(subtask)

        instance.subtasks.set(updated_subtasks)

        return instance