# from rest_framework import generics
# from .models import Task
# from .serializers import TaskSerializer
# from rest_framework.response import Response
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
# from rest_framework.decorators import api_view
# from rest_framework.views import APIView
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework import status
# from django.shortcuts import get_object_or_404
# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from rest_framework.generics import RetrieveUpdateAPIView
# from rest_framework import authentication, permissions
# from django.contrib.auth import logout
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt


# @api_view(['POST'])
# def create_user(request):
#     if request.method == 'POST':
#         username = request.data.get('newUsername')
#         password = request.data.get('newPassword')
#         email = request.data.get('newEmail')
#         if not username:
#             return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
#         if User.objects.filter(username=username).exists():
#             return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
#         if email:
#             if User.objects.filter(email=email).exists():
#                 return Response({'error': 'Email already exists!'}, status=status.HTTP_400_BAD_REQUEST)
#         if not password:
#             return Response({'error': 'Password is required!'}, status=status.HTTP_400_BAD_REQUEST)
#         user = User.objects.create_user(username=username, password=password, email=email)
#         return Response({'user_id': user.id, 'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)
#     else:
#         return Response({'error': 'Error 405'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



# class CustomLoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})


# class UserIdByUsernameView(APIView):
#     def get(self, request, username):
#         try:
#             user = User.objects.get(username=username)
#             return Response({'user_id': user.pk})
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# class TaskListView(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     # permission_classes = [permissions.IsAdminUser]
    
#     def get(self, request):
#         tasks = Task.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
# class TaskDetailView(APIView):
    
#     def delete(self, request, pk):
#         try:
#             task = Task.objects.get(pk=pk)
#             task.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Task.DoesNotExist:
#             return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

 
   
# class TaskDetailDropView(RetrieveUpdateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

#     def put(self, request, pk, format=None):
#         try:
#             task = Task.objects.get(pk=pk)
#         except Task.DoesNotExist:
#             return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = TaskSerializer(instance=task, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# class TaskDetailEdit(RetrieveUpdateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

#     def put(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)


# @csrf_exempt
# def logout_view(request):
#     print('request',request)
#     if request.method == 'POST':
#         logout(request)
#         return JsonResponse({'message': 'Logout successful'})
#     else:
#         return JsonResponse({'error': 'Invalid method'}, status=405)



# def get_task_details(request, task_id):
#     task = get_object_or_404(Task, id=task_id)
#     created_by_username = task.created_by.username
#     data = {
#         'title': task.title,
#         'description': task.description,
#         'column': task.column,
#         'task_index': task.task_index,
#         'created_by': created_by_username,
#         'created_at': task.created_at,
#         'updated_at': task.updated_at
#     }
#     return JsonResponse(data)







from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404
from rest_framework import authentication, permissions
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class CreateUserView(APIView):
    def post(self, request):
        username = request.data.get('newUsername')
        password = request.data.get('newPassword')
        email = request.data.get('newEmail')

        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if email and User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists!'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'error': 'Password is required!'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({'user_id': user.id, 'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)


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
    # permission_classes = [permissions.IsAuthenticated]

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
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)


class TaskDetailDropView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(instance=task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailEdit(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(instance=task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful'})
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)


def get_task_details(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    created_by_username = task.created_by.username
    data = {
        'title': task.title,
        'description': task.description,
        'column': task.column,
        'task_index': task.task_index,
        'created_by': created_by_username,
        'created_at': task.created_at,
        'updated_at': task.updated_at
    }
    return JsonResponse(data)








