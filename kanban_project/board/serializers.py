from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if data['task_index'] is None:
    #         data['task_index'] = 0
    #     return data