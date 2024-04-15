"""
URL configuration for kanban_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
# from board.views import TaskListView,LoginView,TaskDetailView,CustomLoginView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('tasks/', TaskListView.as_view(), name='task-list'),
#     path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
#     path('login/', CustomLoginView.as_view(), name='login'),
# ]


from django.contrib import admin
from django.urls import path
from board.views import TaskListView, TaskDetailView, CustomLoginView,TaskDetailDropView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    # path('tasks/<int:pk>/', TaskDetailDropView.as_view(), name='task-detail-drop'),
    # path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    
    path('tasks/drop/<int:pk>/', TaskDetailDropView.as_view(), name='task-detail-drop'),
    path('tasks/detail/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    
    path('login/', CustomLoginView.as_view(), name='login'),
]

# function fetchTasks() {
#     const token = localStorage.getItem('token');
#     if (!token) {
#         console.error('Token not found in localStorage');
#         return;
#     }

#     fetch('http://127.0.0.1:8000/tasks/', {
#         method: 'GET',
#         headers: {
#             'Content-Type': 'application/json',
#             'Authorization': `Bearer ${token}` // Verwenden Sie das Token im Authorization-Header
#         }
#     })
#     .then(response => response.json())
#     .then(data => {
#         // Verarbeiten Sie die Antwort vom Server
#         console.log('Tasks:', data);
#     })
#     .catch(error => {
#         console.error('Error fetching tasks:', error);
#     });
# }
