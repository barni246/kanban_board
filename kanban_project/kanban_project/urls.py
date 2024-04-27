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


from django.contrib import admin
from django.urls import path
from board.views import (
    CustomLoginView,
    UserIdByUsernameView,
    logout_view,
    CreateUserView, 
     get_task,
     TaskView,
     TaskUpdateView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('create_user/', CreateUserView.as_view(), name='CreateUserView'),
    path('logout/', logout_view, name='logout'),
    path('tasks/', TaskView.as_view(), name='task-list'),
    path('tasks/<int:task_id>/', get_task, name='task-details'),
    path('tasks/update/<int:pk>/', TaskUpdateView.as_view(), name='task-update-delete'),
    path('user_id_by_username/<str:username>/', UserIdByUsernameView.as_view(), name='user-id-by-username'),
    
]
