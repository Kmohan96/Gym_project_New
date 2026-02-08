from django.urls import path
from .views import admin_login, admin_dashboard, admin_users, approve_user
from .views import AdminDashboardView
urlpatterns = [
    path("login/", admin_login),
    path("dashboard/",  AdminDashboardView.as_view()),
    path("users/", admin_users),
    path("users/approve/<int:profile_id>/", approve_user),
   
]