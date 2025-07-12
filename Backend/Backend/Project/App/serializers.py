from rest_framework import serializers
from .models import CustomUser, Skill, UserSkill, SwapRequest
from django.contrib.auth import authenticate
from .models import Feedback

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name', 'location', 'profile_photo', 'availability', 'is_private']

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        data['user'] = user
        return data
    

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

class UserSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer()

    class Meta:
        model = UserSkill
        fields = ['id', 'skill', 'skill_type']



class CreateUserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = ['id', 'user', 'skill', 'skill_type']


class SwapRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)
    offered_skill = SkillSerializer(read_only=True)
    wanted_skill = SkillSerializer(read_only=True)

    class Meta:
        model = SwapRequest
        fields = [
            'id', 'from_user', 'to_user',
            'offered_skill', 'wanted_skill',
            'status', 'created_at'
        ]

class CreateSwapRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwapRequest
        fields = ['to_user', 'offered_skill', 'wanted_skill']



class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['from_user']

class PublicUserSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'location', 'availability', 'profile_photo', 'skills']

    def get_skills(self, obj):
        skills = UserSkill.objects.filter(user=obj)
        return UserSkillSerializer(skills, many=True).data
    

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'profile_photo']

        

class CustomUserSerializer(serializers.ModelSerializer):
    skills_offered = serializers.SerializerMethodField()
    skills_wanted = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'name',
            'email',
            'location',
            'availability',
            'profile_photo',
            'is_private',
            'skills_offered',
            'skills_wanted',
        ]

    def get_profile_photo(self, obj):
        request = self.context.get('request')
        if obj.profile_photo:
            return request.build_absolute_uri(obj.profile_photo.url)
        return None

    def get_skills_offered(self, obj):
        return list(obj.userskill_set.filter(type='offered').values_list('skill__name', flat=True))

    def get_skills_wanted(self, obj):
        return list(obj.userskill_set.filter(type='wanted').values_list('skill__name', flat=True))