from rest_framework import serializers
from .models import Client, HealthProgram, Enrollment

class HealthProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProgram
        fields = ['id', 'name', 'description', 'created_at', 'status']

class EnrollmentSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source='program.name', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'program', 'program_name', 'enrollment_date', 'status', 'notes']

class ClientSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(read_only=True)
    enrollments = EnrollmentSerializer(source='enrollment_set', many=True, read_only=True)

    class Meta:
        model = Client
        fields = [
            'id', 'first_name', 'last_name', 'date_of_birth', 'age',
            'gender', 'phone_number', 'email', 'address',
            'registration_date', 'last_updated', 'enrollments'
        ]

class ClientBasicSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'phone_number'] 