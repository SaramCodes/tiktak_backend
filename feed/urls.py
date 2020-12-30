from django.urls import path
from . import views
urlpatterns = [
    path('', views.PostListCreateView.as_view(), name="post-list-create-view"),
    path('<int:pk>/', views.PostDetailView.as_view(), name="post-detail-view"),
    path('<int:pk>/comment', views.CommentCreateView.as_view(), name="comment-create-view"),
]