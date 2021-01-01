from django.urls import path
from . import views
urlpatterns = [
    path('', views.UserRegisterView.as_view(), name="user-register-view"),
    path('<int:pk>/', views.UserRetrieveView.as_view(), name="user-retrieve-view"),
    path('<int:pk>/follow', views.UserFollowView.as_view(), name="user-follow-view"),
    path('<int:pk>/unfollow', views.UserUnfollowView.as_view(), name="user-unfollow-view"),
    path('<int:pk>/followers', views.UserFollowersRetrieveView.as_view(), name="user-retrieve-followers-view"),
    path('<int:pk>/following', views.UserFollowingRetrieveView.as_view(), name="user-retrieve-following-view"),
    path('profile/<int:pk>', views.UserUpdateView.as_view(), name="user-update-view"),
    path('profile/<int:pk>/image', views.UserImageUpdateView.as_view(), name="user-image-update-view"),
]