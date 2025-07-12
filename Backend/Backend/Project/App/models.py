from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, name, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    profile_photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    availability = models.CharField(max_length=100, blank=True, null=True)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.name

# Skill Model
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# User Skills
class UserSkill(models.Model):
    SKILL_TYPE_CHOICES = (
        ('offered', 'Offered'),
        ('wanted', 'Wanted'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    skill_type = models.CharField(max_length=10, choices=SKILL_TYPE_CHOICES)

    class Meta:
        unique_together = ('user', 'skill', 'skill_type')

# Swap Request Model
class SwapRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )

    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_swaps')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_swaps')
    offered_skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, related_name='offered_in_swaps')
    wanted_skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, related_name='wanted_in_swaps')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} ➝ {self.to_user} ({self.status})"

#Feeback
class Feedback(models.Model):
    swap = models.OneToOneField(SwapRequest, on_delete=models.CASCADE)
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='feedback_given')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='feedback_received')
    rating = models.PositiveIntegerField(default=0)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Rating by {self.from_user.name} to {self.to_user.name}"

