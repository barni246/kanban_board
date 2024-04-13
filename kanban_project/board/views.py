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


from rest_framework import status

class TaskDetailView(generics.RetrieveUpdateAPIView):
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






class LoginView(ObtainAuthToken):
  def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

    
class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
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
        
    