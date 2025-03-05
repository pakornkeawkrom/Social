from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, Http404
from .models import Post, Comment, Share
from .forms import PostForm, CommentForm
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile 

@login_required
def feed_view(request):
    posts = Post.objects.all()
    shares = Share.objects.all()
    item_data_list = []

    for post in posts:
        item_data_list.append({'item': post, 'type': 'post'})
    for share in shares:
        item_data_list.append({'item': share, 'type': 'share'})

    item_data_list.sort(key=lambda item: item['item'].created_at, reverse=True)

    return render(request, 'posts/feed.html', {'items': item_data_list})

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            image = request.FILES.get("image")
            if image:
                img = Image.open(image)
                max_width = 1024
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.LANCZOS)
                output = BytesIO()
                img.save(output, format='JPEG', quality=80)
                output.seek(0)
                image = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    "%s.jpg" % image.name.split('.')[0],
                    'image/jpeg',
                    output.tell,
                    None,
                )
                post.image = image
            post.save()
            return redirect("posts:feed")
        else:
            print(form.errors)
    else:
        form = PostForm()
    return render(request, "posts/create_post.html", {'form': form})

@login_required
def like_post(request, post_id):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        try:
            post = get_object_or_404(Post, id=post_id)
            if request.user in post.liked_by.all():
                post.liked_by.remove(request.user)
                liked = False
            else:
                post.liked_by.add(request.user)
                liked = True
            likes_count = post.liked_by.count()
        except Http404:
            try:
                share = get_object_or_404(Share, id=post_id)
                if request.user in share.liked_by.all():
                    share.liked_by.remove(request.user)
                    liked = False
                else:
                    share.liked_by.add(request.user)
                    liked = True
                likes_count = share.liked_by.count()
            except Http404:
                return JsonResponse({"error": "Post or Share not found"}, status=404)
        return JsonResponse({
            "likes": likes_count,
            "liked": liked,
            "success": True
        })
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def add_comment(request, post_id):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        text = request.POST.get("text")
        if text:
            try:
                post = get_object_or_404(Post, id=post_id)
                comment = Comment.objects.create(user=request.user, post=post, text=text)
            except Http404:
                try:
                    share = get_object_or_404(Share, id=post_id)
                    comment = Comment.objects.create(user=request.user, share=share, text=text)
                except Http404:
                    return JsonResponse({"error": "Post or Share not found"}, status=404)
            return JsonResponse({
                "success": True,
                "comment": {
                    "id": comment.id,
                    "user": comment.user.username,
                    "text": comment.text,
                    "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            })
        else:
            return JsonResponse({"error": "Comment text is required"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # ✅ ใช้ `Share.objects.create()` แทน `Post.objects.create()`
    new_share = Share.objects.create(
        user=request.user,
        post=post,
        content=f"แชร์โพสต์ของ {post.user.username}",
        image=post.image  # ✅ ถ้าต้องการให้แชร์รูปภาพด้วย
    )

    # ✅ อัปเดตตัวนับจำนวนแชร์
    post.share_count += 1
    post.save()

    return redirect("posts:feed")  # ✅ ตรวจสอบ namespace
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        raise PermissionDenied
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:feed')
        else:
            print(form.errors)
    else:
        form = PostForm(instance=post)
    return render(request, "posts/edit_post.html", {'form': form})

@login_required
def confirm_delete_post(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        is_share = False
    except:
        share = get_object_or_404(Share, id=post_id)
        post = share.post
        is_share = True
    if (not is_share and post.user != request.user) or (is_share and share.user != request.user):
        raise PermissionDenied
    if request.method == 'POST':
        if is_share:
            share.delete()
        else:
            post.delete()
        return redirect('posts:feed')
    return render(request, 'posts/delete_post.html', {'post': post, 'is_share': is_share})

@login_required
def delete_share(request, share_id):
    share = get_object_or_404(Share, id=share_id)
    if share.user != request.user:
        raise PermissionDenied
    share.delete()
    return redirect('posts:feed')

@staff_member_required
def manage_posts(request):
    posts = Post.objects.all()
    shares = Share.objects.all()
    items = list(posts) + list(shares)  # รวมทั้งโพสต์และแชร์เข้าไปในรายการ
    items.sort(key=lambda x: x.created_at, reverse=True)  # เรียงตามวันที่ใหม่สุด

    return render(request, "posts/manage_posts.html", {"items": items})

@staff_member_required
def delete_post_admin(request, post_id):
    post = None

    # ตรวจสอบว่าเป็น Post หรือ Share
    if Post.objects.filter(id=post_id).exists():
        post = get_object_or_404(Post, id=post_id)
    elif Share.objects.filter(id=post_id).exists():
        post = get_object_or_404(Share, id=post_id)

    if post:
        post.delete()
    
    return redirect('posts:manage_posts')  # กลับไปที่หน้าจัดการโพสต์