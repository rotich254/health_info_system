from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Client, HealthProgram, Enrollment
from .serializers import (
    ClientSerializer, ClientBasicSerializer,
    HealthProgramSerializer, EnrollmentSerializer
)

# Create your views here.

class HealthProgramViewSet(viewsets.ModelViewSet):
    queryset = HealthProgram.objects.all()
    serializer_class = HealthProgramSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'phone_number', 'email']

    def get_serializer_class(self):
        if self.action == 'list':
            return ClientBasicSerializer
        return ClientSerializer

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        client = self.get_object()
        program_id = request.data.get('program_id')
        
        if not program_id:
            return Response(
                {'error': 'program_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        program = get_object_or_404(HealthProgram, id=program_id)
        
        # Check if enrollment already exists
        enrollment, created = Enrollment.objects.get_or_create(
            client=client,
            program=program,
            defaults={'status': 'ACTIVE'}
        )

        if not created:
            return Response(
                {'error': 'Client is already enrolled in this program'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        client = self.get_object()
        serializer = ClientSerializer(client)
        return Response(serializer.data)

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.query_params.get('client_id', None)
        program_id = self.request.query_params.get('program_id', None)

        if client_id:
            queryset = queryset.filter(client_id=client_id)
        if program_id:
            queryset = queryset.filter(program_id=program_id)

        return queryset
