from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """ ให้สิทธิ์เฉพาะ Admin เท่านั้น """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff  # ใช้ `is_staff` เพื่อตรวจสอบว่าเป็น Admin หรือไม่
