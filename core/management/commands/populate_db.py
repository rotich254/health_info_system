# python manage.py populate_db --clients 100 --programs 5

import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Client, HealthProgram, Enrollment

class Command(BaseCommand):
    help = 'Populates the database with sample clients and health programs'

    def add_arguments(self, parser):
        parser.add_argument('--clients', type=int, default=100, help='Number of clients to create')
        parser.add_argument('--programs', type=int, default=5, help='Number of health programs to create')
        parser.add_argument('--active-ratio', type=float, default=0.7, help='Ratio of programs that should be active (0.0-1.0)')

    def handle(self, *args, **options):
        num_clients = options['clients']
        num_programs = options['programs']
        active_ratio = min(max(options['active_ratio'], 0.0), 1.0)  # Ensure between 0 and 1
        
        self.stdout.write(self.style.SUCCESS(f'Starting database population...'))
        
        # Create health programs
        self.create_health_programs(num_programs, active_ratio)
        
        # Create clients
        self.create_clients(num_clients)
        
        # Enroll clients in programs
        self.enroll_clients()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database!'))
    
    def create_health_programs(self, count, active_ratio):
        programs = [
            {
                'name': 'Tuberculosis Control Program',
                'description': 'A comprehensive program for TB prevention, detection, and treatment.'
            },
            {
                'name': 'Malaria Prevention',
                'description': 'Program focused on malaria prevention, including bed nets and prophylaxis.'
            },
            {
                'name': 'HIV/AIDS Care',
                'description': 'Integrated care program for HIV/AIDS patients, including ARV therapy.'
            },
            {
                'name': 'Maternal Health',
                'description': 'Pre and post-natal care for expectant mothers and newborns.'
            },
            {
                'name': 'Child Immunization',
                'description': 'Routine immunization program for children under 5 years.'
            },
            {
                'name': 'Diabetes Management',
                'description': 'Management and care for patients with diabetes, including diet and medication.'
            },
            {
                'name': 'Hypertension Control',
                'description': 'Program for monitoring and controlling high blood pressure.'
            },
            {
                'name': 'Mental Health Support',
                'description': 'Counseling and therapy for mental health issues.'
            }
        ]
        
        # Use only as many as requested
        program_data = programs[:min(count, len(programs))]
        
        # If more programs requested than in our predefined list, create generic ones
        for i in range(len(program_data), count):
            program_data.append({
                'name': f'Health Program {i+1}',
                'description': f'Description for Health Program {i+1}'
            })
        
        created_count = 0
        active_count = 0
        completed_count = 0
        discontinued_count = 0
        
        for data in program_data:
            # Avoid duplicates
            if not HealthProgram.objects.filter(name=data['name']).exists():
                # Determine status based on active_ratio
                rand_val = random.random()
                if rand_val < active_ratio:
                    status = 'ACTIVE'
                    active_count += 1
                elif rand_val < active_ratio + ((1 - active_ratio) / 2):
                    status = 'COMPLETED'
                    completed_count += 1
                else:
                    status = 'DISCONTINUED'
                    discontinued_count += 1
                
                # Add status to the data
                data['status'] = status
                
                # Create the program
                HealthProgram.objects.create(**data)
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Created {created_count} health programs: '
            f'{active_count} active, {completed_count} completed, {discontinued_count} discontinued'
        ))
    
    def create_clients(self, count):
        # Sample data for random generation
        first_names = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'Robert', 'Lisa', 
                      'William', 'Mary', 'James', 'Jennifer', 'Charles', 'Elizabeth', 'Thomas', 
                      'Patricia', 'Daniel', 'Linda', 'Paul', 'Barbara', 'Mark', 'Susan', 'Donald',
                      'Jessica', 'George', 'Karen', 'Kenneth', 'Nancy', 'Steven', 'Margaret']
        
        last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson',
                      'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin',
                      'Thompson', 'Garcia', 'Martinez', 'Robinson', 'Clark', 'Rodriguez', 'Lewis', 
                      'Lee', 'Walker', 'Hall', 'Allen', 'Young', 'Hernandez', 'King']
        
        domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'example.com']
        
        addresses = [
            '123 Main St, Cityville',
            '456 Oak Avenue, Townsburg',
            '789 Pine Road, Villageton',
            '321 Maple Drive, Hamletville',
            '654 Cedar Lane, Boroughtown',
            '987 Elm Boulevard, Districtville',
            '159 Spruce Court, Regionton',
            '753 Birch Path, Provincetown',
            '852 Walnut Way, Countyton',
            '426 Cherry Street, Stateville'
        ]
        
        created_count = 0
        for i in range(count):
            # Generate random data
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            
            # Generate a date of birth between 18 and 80 years ago
            days_in_year = 365.25  # accounting for leap years
            max_age_days = int(80 * days_in_year)
            min_age_days = int(18 * days_in_year)
            random_days = random.randint(min_age_days, max_age_days)
            dob = date.today() - timedelta(days=random_days)
            
            # Generate other fields
            gender = random.choice(['M', 'F', 'O'])
            phone = f'+1{random.randint(2000000000, 9999999999)}'
            email = f'{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}'
            address = random.choice(addresses)
            
            # Create client
            Client.objects.create(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=dob,
                gender=gender,
                phone_number=phone,
                email=email,
                address=address
            )
            created_count += 1
            
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} clients'))
    
    def enroll_clients(self):
        # Get all clients and ACTIVE programs only
        clients = Client.objects.all()
        active_programs = HealthProgram.objects.filter(status='ACTIVE')
        
        if not clients or not active_programs:
            self.stdout.write(self.style.WARNING('No clients or active programs to enroll'))
            return
        
        enrollment_count = 0
        # Enroll each client in 1-3 random ACTIVE programs
        for client in clients:
            # Determine how many programs this client will join (1-3)
            num_enrollments = random.randint(1, min(3, active_programs.count()))
            
            # Randomly select programs without repetition
            selected_programs = random.sample(list(active_programs), num_enrollments)
            
            for program in selected_programs:
                # Create enrollment with a random status
                status = random.choice(['ACTIVE', 'COMPLETED', 'DISCONTINUED'])
                
                # Random enrollment date in the past year
                days_ago = random.randint(0, 365)
                enrollment_date = timezone.now() - timedelta(days=days_ago)
                
                # Create the enrollment if it doesn't exist
                enrollment, created = Enrollment.objects.get_or_create(
                    client=client,
                    program=program,
                    defaults={
                        'status': status,
                        'enrollment_date': enrollment_date,
                        'notes': f'Automatically generated enrollment for testing'
                    }
                )
                
                if created:
                    enrollment_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {enrollment_count} client enrollments')) 