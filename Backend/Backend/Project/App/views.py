from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from App.serializers import CurrentUserSerializer
from .models import Skill, UserSkill, SwapRequest,Feedback
from .serializers import (
    UserSerializer, SignupSerializer, LoginSerializer,
    SkillSerializer, UserSkillSerializer, CreateUserSkillSerializer,
    SwapRequestSerializer, CreateSwapRequestSerializer,FeedbackSerializer,CustomUserSerializer
)

from django.contrib.auth import authenticate

CustomUser = get_user_model()


def homePage(request):
    return render(request,'index.html')

class SignupAPIView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({
                "message": "Login successful",
                "user": UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]


class SkillListCreateAPIView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.AllowAny]


class MySkillsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        skills = UserSkill.objects.filter(user=request.user)
        serializer = UserSkillSerializer(skills, many=True)
        return Response(serializer.data)


class AddUserSkillAPIView(generics.CreateAPIView):
    serializer_class = CreateUserSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeleteUserSkillAPIView(generics.DestroyAPIView):
    queryset = UserSkill.objects.all()
    serializer_class = CreateUserSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CreateSwapRequestAPIView(generics.CreateAPIView):
    serializer_class = CreateSwapRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)


class MySwapRequestsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        swaps = SwapRequest.objects.filter(
            from_user=request.user
        ) | SwapRequest.objects.filter(to_user=request.user)
        serializer = SwapRequestSerializer(swaps, many=True)
        return Response(serializer.data)


class UpdateSwapStatusAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            swap = SwapRequest.objects.get(pk=pk, to_user=request.user)
        except SwapRequest.DoesNotExist:
            return Response({'error': 'Not found or unauthorized'}, status=404)

        status_choice = request.data.get("status")
        if status_choice not in ['accepted', 'rejected']:
            return Response({'error': 'Invalid status'}, status=400)

        swap.status = status_choice
        swap.save()
        return Response({'message': f'Swap {status_choice}'})


class CancelSwapRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            swap = SwapRequest.objects.get(pk=pk, from_user=request.user)
        except SwapRequest.DoesNotExist:
            return Response({'error': 'Swap not found'}, status=404)

        swap.status = 'cancelled'
        swap.save()
        return Response({'message': 'Swap cancelled'})


class FeedbackCreateAPIView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)


# Get Feedback for a user
class UserFeedbackListAPIView(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Feedback.objects.filter(to_user__id=user_id)



# Public Fetch
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter
from App.serializers import PublicUserSerializer

class PublicUserListAPIView(ListAPIView):
    queryset = CustomUser.objects.filter(is_private=False)
    serializer_class = PublicUserSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'location', 'userskill__skill__name']

class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CurrentUserSerializer(request.user, context={"request": request})
        return Response(serializer.data)
    
class UserDetailByEmailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        serializer = CustomUserSerializer(user, context={"request": request})
        return Response(serializer.data)

