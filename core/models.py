from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class HealthProgram(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('DISCONTINUED', 'Discontinued')
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    def __str__(self):
        return self.name
    
    @property
    def is_active(self):
        return self.status == 'ACTIVE'

class Client(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField()
    registration_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    programs = models.ManyToManyField(HealthProgram, through='Enrollment')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def clean(self):
        # Validate that date of birth is not in the future
        if self.date_of_birth and self.date_of_birth > timezone.now().date():
            raise ValidationError({'date_of_birth': 'Date of birth cannot be in the future.'})
        super().clean()
    
    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

class Enrollment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    program = models.ForeignKey(HealthProgram, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('DISCONTINUED', 'Discontinued')
    ], default='ACTIVE')
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['client', 'program']

    def __str__(self):
        return f"{self.client} - {self.program}"
