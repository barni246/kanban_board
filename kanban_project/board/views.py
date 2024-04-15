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
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.http import Http404 



class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        tasks = self.get_queryset()
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        username = request.data.get('created_by')
        user = User.objects.get(username=username)
        task_data = request.data
        task_data['created_by'] = user.id
        serializer = self.get_serializer(data=task_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    # def delete(self, request, pk, format=None):
    #     try:
    #         task = Task.objects.get(pk=pk)
    #         if task.created_by != request.user:
    #             return Response({"error": "You are not authorized to delete this task."}, status=status.HTTP_403_FORBIDDEN)
    #     except Task.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    #     task.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class TaskDetailDropView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def put(self, request, pk, format=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if 'title' in request.data:
            task.title = request.data['title']
        if 'description' in request.data:
            task.description = request.data['description']
        if 'column' in request.data:
            task.column = request.data['column']
        if 'task_index' in request.data:
            task.task_index = request.data['task_index']
        task.save()

        return Response(TaskSerializer(task).data)

class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})



class TaskDetailView(APIView):
    
    
    # def get_object(self, pk):
    #     try:
    #         return Task.objects.get(pk=pk)
    #     except Task.DoesNotExist:
    #         raise Http404

    # def put(self, request, pk, format=None):
    #     task = self.get_object(pk)
    #     serializer = TaskSerializer(task, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

















# class TaskDetailView(generics.RetrieveUpdateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     def put(self, request, pk, format=None):
#         # Versuchen Sie, den Task mit der angegebenen ID zu erhalten
#         try:
#             task = Task.objects.get(pk=pk)
#         except Task.DoesNotExist:
#             return Response({"error": "Task not found"})
#         print("Request data:", request.data)
#         # Aktualisieren Sie die Daten des Tasks gemäß den Anforderungen
#         if 'title' in request.data:
#             task.title = request.data['title']
#             print("task.title:", task.title)
#         if 'description' in request.data:
#             task.description = request.data['description']
#         if 'column' in request.data:
#             task.column = request.data['column']
#         if 'task_index' in request.data:
#             task.taskIndex = request.data['task_index']
#         task.save()






# class TaskListView(generics.ListCreateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     # permission_classes = [IsAuthenticated]
    
#     def get(self, request, *args, **kwargs):
#         tasks = self.get_queryset()
#         serializer = self.get_serializer(tasks, many=True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         username = request.data.get('created_by')
#         user = User.objects.get(username=username)
#         task_data = request.data
#         task_data['created_by'] = user.id
#         serializer = self.get_serializer(data=task_data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
#     def delete(self, request, pk, format=None):
#      try:
#         task = Task.objects.get(pk=pk)
#         # Überprüfen, ob der aktuelle Benutzer der Autor der Aufgabe ist
#         if task.created_by != request.user:
#             return Response({"error": "You are not authorized to delete this task."}, status=status.HTTP_403_FORBIDDEN)
#      except Task.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#      task.delete()
#      return Response(status=status.HTTP_204_NO_CONTENT)

    
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.response import Response

# class CustomLoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})
  
    
    # eddig
    
    
# class TaskView(APIView):
#     def get(self, request, format=None):
#         tasks = Task.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk, format=None):
#         task = get_object_or_404(Task, pk=pk)
#         serializer = TaskSerializer(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         task = get_object_or_404(Task, pk=pk)
#         task.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class TaskDetailView(generics.RetrieveUpdateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

#     def put(self, request, pk, format=None):
#         try:
#             task = Task.objects.get(pk=pk)
#         except Task.DoesNotExist:
#             return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         if 'title' in request.data:
#             task.title = request.data['title']
#         if 'description' in request.data:
#             task.description = request.data['description']
#         if 'column' in request.data:
#             task.column = request.data['column']
#         if 'task_index' in request.data:
#             task.task_index = request.data['task_index']
#         task.save()

#         return Response(TaskSerializer(task).data)

