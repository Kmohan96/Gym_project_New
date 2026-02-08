from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from .models import UserProfile, Trainer, DailyUpdate


# =========================
# USER REGISTRATION
# =========================
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        username = data.get("username")
        password = data.get("password")
        age = data.get("age")
        height = data.get("height")
        weight = data.get("weight")
        goal = data.get("goal")
        gym_type = data.get("gym_type")

        if not username or not password:
            return Response(
                {"error": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            age=age,
            height=height,
            weight=weight,
            goal=goal,
            gym_type=gym_type,
            approved=False
        )

        return Response(
            {"message": "User registered successfully. Waiting for admin approval."},
            status=status.HTTP_201_CREATED
        )


# =========================
# USER PROFILE (JWT)
# =========================
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)

        return Response({
            "username": request.user.username,
            "approved": profile.approved,
            "goal": profile.goal,
            "trainer": profile.trainer.trainer_id if profile.trainer else None
        })


# =========================
# ADMIN – CREATE TRAINER
# =========================
class CreateTrainerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        trainer_id = request.data.get("trainer_id")

        if not username or not password or not trainer_id:
            return Response(
                {"error": "Missing data"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username)
            profile = UserProfile.objects.get(user=user)
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        user.set_password(password)
        user.save()

        trainer, _ = Trainer.objects.update_or_create(
            user=user,
            defaults={"trainer_id": trainer_id}
        )

        profile.trainer = trainer
        profile.approved = True
        profile.save()

        return Response(
            {"message": "Trainer created successfully"},
            status=status.HTTP_201_CREATED
        )


# =========================
# TRAINER – USERS LIST
# =========================
class TrainerUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trainer = Trainer.objects.get(user=request.user)

        profiles = UserProfile.objects.filter(trainer=trainer, approved=True)

        users = [
            {
                "username": p.user.username,
                "goal": p.goal,
                "age": p.age
            }
            for p in profiles
        ]

        return Response({"users": users})


# =========================
# TRAINER – ADD DAILY UPDATE
# =========================
class AddDailyUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        trainer = Trainer.objects.get(user=request.user)

        username = request.data.get("username")
        date = request.data.get("date")
        diet = request.data.get("diet")
        attendance = request.data.get("attendance")
        description = request.data.get("description")

        user = User.objects.get(username=username)

        DailyUpdate.objects.create(
            trainer=trainer,
            user=user,
            date=date,
            diet=diet,
            attendance=attendance,
            description=description
        )

        return Response(
            {"message": "Daily update added"},
            status=status.HTTP_201_CREATED
        )


# =========================
# USER – VIEW UPDATES
# =========================
class UserUpdatesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        updates = DailyUpdate.objects.filter(
            user=request.user
        ).order_by("-date")

        data = [
            {
                "date": u.date,
                "diet": u.diet,
                "attendance": u.attendance,
                "description": u.description
            }
            for u in updates
        ]

        present_days = updates.filter(attendance=True).count()

        return Response({
            "updates": data,
            "present_days": present_days
        })
