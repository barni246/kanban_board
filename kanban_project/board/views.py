from django.shortcuts import render
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import authentication, permissions
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        username = request.data.get('newUsername')
        password = request.data.get('newPassword')
        email = request.data.get('newEmail')
        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if email:
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists!'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'error': 'Password is required!'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({'user_id': user.id, 'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Error 405'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserIdByUsernameView(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            return Response({'user_id': user.pk})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class TaskListView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
class TaskDetailView(APIView):
    
    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

 
   
class TaskDetailDropView(RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def put(self, request, pk, format=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TaskSerializer(instance=task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def logout_view(request):
    print('request',request)
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful'})
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)















