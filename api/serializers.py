from rest_framework import serializers

from dashboard.models import Designation, Todo

class DesignationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Designation
        fields = ['name', 'position', 'gender', 'date_of_birth']


class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = '__all__'
