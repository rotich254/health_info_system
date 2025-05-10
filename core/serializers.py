from rest_framework import serializers
from .models import Client, HealthProgram, Enrollment
from django.core.exceptions import ValidationError

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
        
    def validate(self, data):
        # Create a temporary instance to call clean method
        instance = Client(**data)
        if self.instance:
            # If updating an existing instance, set the instance attributes
            for attr, value in data.items():
                setattr(self.instance, attr, value)
            instance = self.instance
        
        # Call the model's clean method
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        
        return data

class ClientBasicSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'phone_number'] 