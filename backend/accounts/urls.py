from django.urls import path
from .views import (
    RegisterUserView,
    UserProfileView,
    CreateTrainerView,
    TrainerUsersView,
    AddDailyUpdateView,
    UserUpdatesView,
)

urlpatterns = [
    path("register/", RegisterUserView.as_view()),
    path("profile/", UserProfileView.as_view()),
    path("trainer/create/", CreateTrainerView.as_view()),
    path("trainer/users/", TrainerUsersView.as_view()),
    path("trainer/daily-update/", AddDailyUpdateView.as_view()),
    path("user/updates/", UserUpdatesView.as_view()),
]
