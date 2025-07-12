from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('user/<int:id>/', UserProfileView.as_view(), name='user-profile'),
    path('skills/', SkillListCreateAPIView.as_view(), name='skills'),
    path('my-skills/', MySkillsAPIView.as_view(), name='my-skills'),
    path('add-skill/', AddUserSkillAPIView.as_view(), name='add-skill'),
    path('delete-skill/<int:pk>/', DeleteUserSkillAPIView.as_view(), name='delete-skill'),
    path('create-swap/', CreateSwapRequestAPIView.as_view(), name='create-swap'),
    path('my-swaps/', MySwapRequestsAPIView.as_view(), name='my-swaps'),
    path('update-swap-status/<int:pk>/', UpdateSwapStatusAPIView.as_view(), name='update-swap-status'),
    path('cancel-swap/<int:pk>/', CancelSwapRequestAPIView.as_view(), name='cancel-swap'),
    path('feedback/create/', FeedbackCreateAPIView.as_view(), name='create-feedback'),
    path('feedback/user/<int:user_id>/', UserFeedbackListAPIView.as_view(), name='user-feedback-list'),
    path('public-users/', PublicUserListAPIView.as_view(), name='public-users'),
    path('current-user/', CurrentUserAPIView.as_view(), name='current-user'),
    path('user-details/', UserDetailByEmailAPIView.as_view(), name='user-details-by-email'),
]