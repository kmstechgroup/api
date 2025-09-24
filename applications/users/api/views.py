import stat
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from urllib3 import response
from ..models import User
from .serializer import UserRegisterSerializer

class UsersAPIView(APIView):
    def get(self, request, pk=None):
            if pk:  # si viene un id en la URL
                try:
                    user = User.objects.get(pk=pk)
                    serializer = UserRegisterSerializer(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                users = User.objects.all()
                serializer = UserRegisterSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        print("📩 Request data:", request.data)
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("❌ Errores del serializer:", serializer.errors)   # 👈 debug
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)