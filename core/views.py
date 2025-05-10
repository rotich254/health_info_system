from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Client, HealthProgram, Enrollment
from .serializers import (
    ClientSerializer, ClientBasicSerializer,
    HealthProgramSerializer, EnrollmentSerializer
)
from django.utils import timezone

# User authentication views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the page the user was trying to access, or home
                next_page = request.GET.get('next', reverse_lazy('index'))
                return HttpResponseRedirect(next_page)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add first name and last name if provided
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            if first_name or last_name or email:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
            
            # Log in the user after registration
            login(request, user)
            messages.success(request, f"Account created for {user.username}!")
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

# Main application views
@login_required
def index(request):
    """
    View function for the home page of the site.
    """
    current_date = timezone.now().date()
    return render(request, 'index.html', {'current_date': current_date})

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

    def create(self, request, *args, **kwargs):
        # Validate date of birth is not in the future
        date_of_birth = request.data.get('date_of_birth')
        if date_of_birth:
            try:
                dob_date = timezone.datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                current_date = timezone.now().date()
                if dob_date > current_date:
                    return Response(
                        {'error': 'Date of birth cannot be in the future.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                return Response(
                    {'error': 'Invalid date format for date of birth.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Validate date of birth is not in the future
        date_of_birth = request.data.get('date_of_birth')
        if date_of_birth:
            try:
                dob_date = timezone.datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                current_date = timezone.now().date()
                if dob_date > current_date:
                    return Response(
                        {'error': 'Date of birth cannot be in the future.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                return Response(
                    {'error': 'Invalid date format for date of birth.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return super().update(request, *args, **kwargs)

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
