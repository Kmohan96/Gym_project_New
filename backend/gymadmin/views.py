from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from accounts.models import UserProfile


# =========================
# ADMIN DASHBOARD
# =========================
class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_superuser:
            return Response(
                {"error": "Not an admin"},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response({
            "admin": request.user.username
        })


# =========================
# LIST ALL USERS
# =========================
class AdminUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_superuser:
            return Response(
                {"error": "Not an admin"},
                status=status.HTTP_403_FORBIDDEN
            )

        profiles = UserProfile.objects.select_related("user").all()

        users = [
            {
                "id": profile.id,
                "username": profile.user.username,
                "goal": profile.goal,
                "approved": profile.approved,
            }
            for profile in profiles
        ]

        return Response({"users": users})


# =========================
# APPROVE USER
# =========================
class ApproveUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_superuser:
            return Response(
                {"error": "Not an admin"},
                status=status.HTTP_403_FORBIDDEN
            )

        profile_id = request.data.get("user_id")

        try:
            profile = UserProfile.objects.get(id=profile_id)
            profile.approved = True
            profile.save()
            return Response({"message": "User approved"})
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
