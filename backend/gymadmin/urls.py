from django.urls import path
from .views import (
    AdminDashboardView,
    AdminUsersView,
    ApproveUserView,
)

urlpatterns = [
    path("dashboard/", AdminDashboardView.as_view()),
    path("users/", AdminUsersView.as_view()),
    path("users/approve/", ApproveUserView.as_view()),
]
