from django.urls import path
from . import views # ✅ Add this line
from .views import (
    register_view, login_view, logout_view, 
    profile_view, user_profile_view, edit_profile, 
    follow_user, unfollow_user, search_users,
    admin_view, delete_user #✅ add admin_view import
)
from .api_views import DeleteUserView  # API

app_name = "users"

urlpatterns = [
    path("register/", register_view, name="register"),  
    path("login/", login_view, name="login"),  
    path("logout/", logout_view, name="logout"),
    # แก้ไข URLs ให้แตกต่างกันระหว่าง profile ของตัวเองและโปรไฟล์คนอื่น
    path("profile/", profile_view, name="profile"),  # สำหรับโปรไฟล์ของตัวเอง
    path("profile/<str:username>/", user_profile_view, name="user_profile"),  # สำหรับโปรไฟล์ของคนอื่น
  # ✅ แสดงโปรไฟล์คนอื่น
    path("edit/", edit_profile, name="edit_profile"),
    path("follow/<int:user_id>/", follow_user, name="follow_user"),
    path("unfollow/<int:user_id>/", unfollow_user, name="unfollow_user"),
    path("search/", search_users, name="search_users"),
    path("api/delete-user/<int:user_id>/", DeleteUserView.as_view(), name="delete_user_api"),
    path("admin/", admin_view, name="admin"),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),  #✅
]
