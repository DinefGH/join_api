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
        fields = ['id', 'task', 'text', 'completed']


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
    subtasks = SubtaskSerializer(many=True, read_only=True)
    creator = serializers.StringRelatedField(read_only=True)  # Displays the string representation of the creator

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'due_date', 'category', 'assigned_to', 'creator', 'subtasks']

    def create(self, validated_data):
        # Pop subtasks data from validated data if it exists
        subtasks_data = validated_data.pop('subtasks', [])
        # Pop assigned_to data to handle after the task creation
        assigned_to_data = validated_data.pop('assigned_to', [])

        # Create the task instance
        task = Task.objects.create(**validated_data)

        # Set the ManyToMany relation for 'assigned_to'
        task.assigned_to.set(assigned_to_data)

        # Create subtasks if subtasks_data is provided
        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)

        return task

    def update(self, instance, validated_data):
        # Pop subtasks data from validated data if it exists
        subtasks_data = validated_data.pop('subtasks', None)
        # Pop assigned_to data to handle after updating the instance
        assigned_to_data = validated_data.pop('assigned_to', None)

        # Update the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Set the ManyToMany relation for 'assigned_to'
        if assigned_to_data is not None:
            instance.assigned_to.set(assigned_to_data)

        # Update or create subtasks
        if subtasks_data is not None:
            for subtask_data in subtasks_data:
                subtask_id = subtask_data.get('id', None)
                if subtask_id:
                    subtask = Subtask.objects.get(id=subtask_id, task=instance)
                    for key, value in subtask_data.items():
                        setattr(subtask, key, value)
                    subtask.save()
                else:
                    Subtask.objects.create(task=instance, **subtask_data)

        return instance