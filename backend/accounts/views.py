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
        goal = data.get("goal")
        gym_type = data.get("gym_type")

        if not username or not password or not goal or not gym_type:
            return Response(
                {"error": "username, password, goal, and gym_type are required"},
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
            goal=goal,
            gym_type=gym_type,
            approved=False   # ⬅ approval logic stays
        )

        return Response(
            {"message": "Registered successfully. Waiting for admin approval."},
            status=status.HTTP_201_CREATED
        )


# =========================
# USER PROFILE (JWT)
# =========================
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.filter(user=request.user).first()

        if not profile:
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not profile.approved:
            return Response(
                {"error": "Account not approved yet"},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(
            {
                "username": request.user.username,
                "approved": profile.approved,
                "goal": profile.goal,
                "trainer": profile.trainer.trainer_id if profile.trainer else None
            },
            status=status.HTTP_200_OK
        )


# =========================
# ADMIN – APPROVE USER + CREATE TRAINER
# =========================
class CreateTrainerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_superuser:
            return Response(
                {"error": "Admin access required"},
                status=status.HTTP_403_FORBIDDEN
            )

        username = request.data.get("username")
        trainer_id = request.data.get("trainer_id")

        if not username or not trainer_id:
            return Response(
                {"error": "username and trainer_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(username=username).first()
        profile = UserProfile.objects.filter(user=user).first()

        if not user or not profile:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        trainer, _ = Trainer.objects.get_or_create(
            user=user,
            defaults={"trainer_id": trainer_id}
        )

        profile.trainer = trainer
        profile.approved = True
        profile.save()

        return Response(
            {"message": "User approved and trainer created"},
            status=status.HTTP_200_OK
        )


# =========================
# TRAINER – USERS LIST
# =========================
class TrainerUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trainer = Trainer.objects.filter(user=request.user).first()

        if not trainer:
            return Response(
                {"error": "You are not a trainer"},
                status=status.HTTP_403_FORBIDDEN
            )

        profiles = UserProfile.objects.filter(trainer=trainer, approved=True)

        return Response(
            [
                {
                    "username": p.user.username,
                    "goal": p.goal,
                    "age": p.age
                }
                for p in profiles
            ],
            status=status.HTTP_200_OK
        )


# =========================
# TRAINER – ADD DAILY UPDATE
# =========================
class AddDailyUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        trainer = Trainer.objects.filter(user=request.user).first()

        if not trainer:
            return Response(
                {"error": "You are not a trainer"},
                status=status.HTTP_403_FORBIDDEN
            )

        username = request.data.get("username")
        date = request.data.get("date")
        diet = request.data.get("diet", "")
        attendance = request.data.get("attendance")
        description = request.data.get("description", "")

        if not username or not date or attendance is None:
            return Response(
                {"error": "username, date, attendance required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(username=username).first()
        profile = UserProfile.objects.filter(
            user=user,
            trainer=trainer,
            approved=True
        ).first()

        if not profile:
            return Response(
                {"error": "User not assigned to you"},
                status=status.HTTP_403_FORBIDDEN
            )

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

        return Response(
            {
                "updates": [
                    {
                        "date": u.date,
                        "diet": u.diet,
                        "attendance": u.attendance,
                        "description": u.description
                    }
                    for u in updates
                ],
                "present_days": updates.filter(attendance=True).count()
            },
            status=status.HTTP_200_OK
        )
