from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.core.exceptions import PermissionDenied


# กำหนด User ให้เป็น CustomUser ที่ถูกต้อง
User = get_user_model()

# สมัครสมาชิก
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("users:register")

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully! You can now login.")
        return redirect("users:login")

    return render(request, "users/register.html")

# เข้าสู่ระบบ
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect("posts:feed")  # ✅ เปลี่ยนเป็น posts:feed แทน social:home
        else:
            messages.error(request, "Invalid credentials")
            return redirect("users:login")

    return render(request, "users/login.html")

# ออกจากระบบ
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("users:login")

# ดูโปรไฟล์ตัวเอง
@login_required
def profile_view(request):
    """แสดงโปรไฟล์ของตัวเอง"""
    return render(request, "users/profile.html", {
        "user_profile": request.user,
        "followers": request.user.followers.all(),
        "following": request.user.following.all(),
    })
    

# ดูโปรไฟล์ของผู้ใช้คนอื่น
def user_profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    followers = user_profile.followers.all()
    following = user_profile.following.all()

    is_following = request.user in followers

    context = {
        "user_profile": user_profile,
        "followers": followers,
        "following": following,
        "is_following": is_following,
    }
    return render(request, "users/profile.html", context)

# แก้ไขโปรไฟล์
@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:profile")  # ✅ กลับไปหน้าโปรไฟล์ตัวเอง
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "users/edit_profile.html", {"form": form})

# ติดตามผู้ใช้
@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id) #✅ ใช้ get_user_model
    if request.user != user_to_follow:
        request.user.follow(user_to_follow)
    return redirect("users:user_profile", username=user_to_follow.username)  # ใช้ username

# เลิกติดตามผู้ใช้
@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id) #✅ ใช้ get_user_model
    if request.user != user_to_unfollow:
        request.user.unfollow(user_to_unfollow)
    return redirect("users:user_profile", username=user_to_unfollow.username)  # ✅ ใช้ username

# ค้นหาผู้ใช้
def search_users(request):
    User = get_user_model() # ✅ ใช้ get_user_model()
    query = request.GET.get("q")
    users = User.objects.filter(username__icontains=query) if query else [] #✅ ใช้ User แทน CustomUser
    
    return render(request, "users/search_results.html", {"users": users, "query": query})

@login_required
def admin_view(request):
    if not request.user.is_admin:
        raise PermissionDenied
    
    users = User.objects.all().order_by("username") #✅ get all user
    
    return render(request, "users/admin.html", {"users": users})

@login_required
def delete_user(request, user_id):
    #✅ ตรวจสอบว่าเป็น Admin หรือไม่
    if not request.user.is_admin:
        raise PermissionDenied

    user_to_delete = get_object_or_404(User, id=user_id)
    #✅ตรวจสอบว่าไม่ใช่กำลังลบตัวเอง
    if user_to_delete == request.user:
        raise PermissionDenied

    if request.method == "POST":
        user_to_delete.delete()
        return redirect('users:admin')  # กลับไปหน้า Admin

    return render(request, "users/delete_user.html", {'user': user_to_delete})