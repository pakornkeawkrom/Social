from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .permissions import IsAdminUser  # นำเข้า Permission

User = get_user_model()

class DeleteUserView(APIView):
    permission_classes = [IsAdminUser]  # ให้เฉพาะแอดมินเข้าถึง

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
