from django.urls import path
from . import views
app_name = "posts"

urlpatterns = [
    path("create/", views.create_post, name="create_post"),
    path("", views.feed_view, name="feed"),
    path("<int:post_id>/like/", views.like_post, name="like_post"),
    path("<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("<int:post_id>/share/", views.share_post, name="share_post"),
    path("<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path("<int:post_id>/delete/", views.confirm_delete_post, name="confirm_delete_post"),
    path("share/<int:share_id>/delete/", views.delete_share, name="delete_share"),
    path('admin/posts/', views.manage_posts, name='manage_posts'),
    path("admin/posts/<int:post_id>/delete/", views.delete_post_admin, name="delete_post_admin"),
]
