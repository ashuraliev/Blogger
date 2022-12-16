from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterUserView, DeleteUserView, UserListView, UserRetrieveView


urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('delete/', DeleteUserView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('user/', UserListView.as_view(), name='user-list'),
    path('retrieve/<int:id>/', UserRetrieveView.as_view(), name='user-retrieve'),
    path('user/', UserListView.as_view(),),
    path('retrieve/<int:pk>/', UserRetrieveView.as_view()),
]
