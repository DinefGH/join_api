from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserDetailsSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Contact
from .forms import ContactForm







User = get_user_model()

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Authentication was successful
            token, created = Token.objects.get_or_create(user=user)
            # Serialize the user data
            user_data = UserDetailsSerializer(user).data
            return Response({"token": token.key, "user": user_data}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
    

class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserDetailsSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/add_contact.html'
    success_url = reverse_lazy('contact_success')  # Adjust as necessary

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user
        return super().form_valid(form)