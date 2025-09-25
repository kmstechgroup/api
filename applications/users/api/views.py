from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from urllib3 import response
from ..models import User
from .serializer import UserRegisterSerializer
from rest_framework.viewsets import ViewSet
class UsersViewSet(ViewSet):
    def list(self, request, pk=None):
                users = User.objects.all()
                serializer = UserRegisterSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
    def retrieve(self, request, pk=None):
                try:
                    user = User.objects.get(pk=pk)
                    serializer = UserRegisterSerializer(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        print("📩 Request data:", request.data)
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)