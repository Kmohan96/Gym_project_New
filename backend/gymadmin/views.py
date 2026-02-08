from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import UserProfile


# ---------------- ADMIN LOGIN ----------------
@csrf_exempt
def admin_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    username = request.POST.get("username")
    password = request.POST.get("password")

    print("Admin login attempt:", username)

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    if not user.is_superuser:
        return JsonResponse({"error": "Not an admin"}, status=403)

    login(request, user)

    return JsonResponse({
        "message": "Admin login successful",
        "admin": user.username
    })


# ---------------- ADMIN DASHBOARD ----------------
def admin_dashboard(request):
    return JsonResponse({
        "message": "Welcome Admin"
    })


# ---------------- LIST USERS ----------------
def admin_users(request):
    profiles = UserProfile.objects.select_related("user").all()

    users = []
    for profile in profiles:
        users.append({
            "id": profile.id,
            "username": profile.user.username,
            "goal": profile.goal,
            "approved": profile.approved,
        })

    return JsonResponse({"users": users})


# ---------------- APPROVE USER (NO CSRF, NO POST) ----------------
def approve_user(request, profile_id):
    try:
        profile = UserProfile.objects.get(id=profile_id)
        profile.approved = True
        profile.save()

        return JsonResponse({"message": "User approved"})
    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "admin": request.user.username
        })
