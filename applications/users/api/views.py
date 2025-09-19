from django.db.models.sql import RawQuery
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import User


class UsersAPIView(APIView):
    def get(self, request, pk=None):
            if pk:  # si viene un id en la URL
                try:
                    user = User.objects.get(pk=pk)
                    return Response(
                        data={"id": user.id_user, "email": user.email, "identificator": user.identificator, "password":user.password},
                        status=status.HTTP_200_OK
                    )
                except User.DoesNotExist:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                users = [{"id": u.id_user, "email": u.email, "identificator": u.identificator} for u in User.objects.all()]
                return Response(data=users, status=status.HTTP_200_OK)
    
    def post(self, request):
        User.objects.create(email=request.data['email'], identificator=request.data['identificator'], password=request.data['password'])
        
        return self.get(request)