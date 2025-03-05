from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image"]
        labels = {
            "content": "",
            "image": "",
        }
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 3, 
                "placeholder": "What’s on your mind?", 
                "class": "form-control",
            }),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and image.size > 5 * 1024 * 1024:  # ✅ จำกัดขนาดไฟล์ที่ 5MB
            raise forms.ValidationError("ไฟล์รูปภาพต้องมีขนาดไม่เกิน 5MB")
        return image

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": ""}
        widgets = {
            "text": forms.TextInput(attrs={
                "placeholder": "Write a comment...",
                "class": "form-control",
                "maxlength": "500",  # ✅ ป้องกันข้อความยาวเกินไป
            }),
        }
