from django.urls import path
from . import views
urlpatterns = [
    path('', views.UserRegisterView.as_view(), name="user-register-view"),
]