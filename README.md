# Health Information System

A comprehensive system for managing client health information, programs, and enrollments designed for healthcare providers. This application allows doctors to manage health programs, register clients, and track client enrollments in various health programs.

![Health Information System](docs/Screenshot%202025-04-25%20131344.png)

## Features

- **User Authentication**: Secure login and registration system
- **Health Program Management**: Create and manage health programs (TB, Malaria, HIV, etc.)
- **Client Registration**: Register and track client information
- **Program Enrollment**: Enroll clients in one or more health programs
- **Client Search**: Easily find clients using search functionality
- **Client Profiles**: View detailed client information and program enrollments
- **REST API**: Access client profiles and other data via API endpoints

## Presentation

Download the full presentation about this system:
- [Health Information System Presentation (PowerPoint)](Health_Info_System_From_HTML.pptx)

## Screenshots

### Login and Registration
![Login Screen](docs/Screenshot%202025-04-25%20131207.png)

### Health Programs Dashboard
![Health Programs](docs/Screenshot%202025-04-25%20131249.png)

### Client Management
![Client List](docs/Screenshot%202025-04-25%20131311.png)

### Client Profile
![Client Profile](docs/Screenshot%202025-04-25%20131322.png)

## Installation Guide

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone or download the project**

   ```bash
   # Clone the repository
   git clone https://github.com/rotich254/health_info_system.git
   cd health_info_system
   ```
   
   Alternatively, you can download and extract the ZIP archive from the [GitHub repository](https://github.com/rotich254/health_info_system.git).

2. **Set up a virtual environment** (recommended)

   Open a terminal/command prompt and navigate to the project folder:

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create an admin user**

   ```bash
   python manage.py createsuperuser
   ```
   
   Follow the prompts to create a username, email, and password.

6. **Start the development server**

   ```bash
   python manage.py runserver
   ```

7. **Access the application**

   Open your web browser and go to: http://127.0.0.1:8000/

## Usage Guide

### Logging In and Registration

1. **Register a new account**
   - Click on the "Register here" link on the login page
   - Fill in your username, email, name, and password
   - Click "Register"

2. **Log in to the system**
   - Enter your username and password
   - Click "Login"

### Health Program Management

1. **View all health programs**
   - Click on "Programs" in the navigation bar
   - View programs sorted by status (Active, Completed, Discontinued)

2. **Add a new health program**
   - Click the "+ Add Program" button
   - Fill in the program name and description
   - Select a status (Active, Completed, or Discontinued)
   - Click "Save Program"

3. **Filter programs by status**
   - Click on the status buttons (All Programs, Active, Completed, Discontinued)
   - View the filtered list of programs

### Client Management

1. **View all clients**
   - Click on "Clients" in the navigation bar
   - Browse the list of registered clients

2. **Register a new client**
   - Click the "+ Register Client" button
   - Fill in the client's personal information
   - Click "Register Client"

3. **Search for clients**
   - Enter a search term in the search box (name, phone number, or email)
   - Click "Search" or press Enter

4. **View client profile**
   - Click on a client's name in the list
   - View the client's personal information and program enrollments

### Managing Client Enrollments

1. **Enroll a client in a program**
   - Open a client's profile
   - Click "Enroll in New Program"
   - Select an active program from the dropdown
   - Click "Enroll Client"

2. **View client enrollments**
   - Open a client's profile
   - Scroll down to the "Enrollments" section
   - View the list of programs the client is enrolled in

## Populating Demo Data

To quickly test the system with demo data, run:

```bash
python manage.py populate_db
```

This will create:
- 100 sample clients with random information
- 5 health programs (TB, Malaria, HIV, etc.)
- Random enrollments of clients in programs

You can customize the amounts by adding parameters:

```bash
python manage.py populate_db --clients 50 --programs 8 --active-ratio 0.6
```

## API Documentation

The system exposes the following API endpoints:

- `/api/programs/` - List all health programs
- `/api/clients/` - List all clients
- `/api/clients/{id}/profile/` - View client profile with enrollments
- `/api/clients/{id}/enroll/` - Enroll client in a program
- `/api/enrollments/` - List all enrollments

All API endpoints require authentication.

## Troubleshooting

### Common Issues

1. **"No such table" error after installation**
   - Make sure you've run the migrations:
     ```
     python manage.py makemigrations
     python manage.py migrate
     ```

2. **Cannot log in with created user**
   - Ensure you're using the correct username and password
   - Try resetting your password through the admin interface

3. **Cannot enroll clients in programs**
   - Verify that you have active health programs in the system
   - Only active programs can be used for enrollment

4. **CSRF token missing or incorrect errors**
   - Make sure your browser has cookies enabled
   - Try clearing your browser cookies and cache

### Getting Help

If you encounter any issues not covered here, please create an issue in the project repository or contact the system administrator.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Developed as part of a health information management system project. 