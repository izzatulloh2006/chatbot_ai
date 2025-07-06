from django.urls import path
from .views import UserListCreateView, UserCRUDView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:user_id>/', UserCRUDView.as_view(), name='user-detail'),
]
