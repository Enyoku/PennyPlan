from django.urls import path

from .views import ChangePasswordView, LoginView, LogoutView, ProfileView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/change-password", ChangePasswordView.as_view, name="change_password"),
    path("logout/", LogoutView.as_view(), name="logout")
]
