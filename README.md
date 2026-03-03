# Hospital Management System (HMS)

A Django-based web application for managing hospital operations including patients, doctors, and appointments.

## Features

- **Patient Management**: Add, update, and manage patient records with personal information
- **Doctor Management**: Maintain a database of doctors with their specializations and contact details
- **Appointment Scheduling**: Book appointments between patients and doctors with automatic conflict detection
- **User Authentication**: Secure login/logout functionality with dashboard access
- **Admin Interface**: Django admin panel for administrative tasks
- **Data Validation**: Prevents double-booking for both patients and doctors

## Project Structure

```
HMS/
├── hms/                      # Main project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL routing
│   ├── views.py             # Core views (home, login, dashboard)
│   ├── decorators.py        # Custom decorators
│   └── wsgi.py              # WSGI configuration
├── patients/                # Patient management app
│   ├── models.py            # Patient model
│   ├── views.py             # Patient views
│   ├── urls.py              # Patient URLs
│   └── forms.py             # Patient forms
├── doctors/                 # Doctor management app
│   ├── models.py            # Doctor model
│   ├── views.py             # Doctor views
│   ├── urls.py              # Doctor URLs
│   └── forms.py             # Doctor forms
├── appointments/            # Appointment management app
│   ├── models.py            # Appointment model
│   ├── views.py             # Appointment views
│   ├── urls.py              # Appointment URLs
│   └── forms.py             # Appointment forms
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── home.html            # Home page
│   ├── public_home.html     # Public landing page
│   ├── login.html           # Login page
│   ├── dashboard.html       # Dashboard
│   ├── patients/            # Patient templates
│   ├── doctors/             # Doctor templates
│   └── appointments/        # Appointment templates
├── manage.py               # Django management script
├── db.sqlite3              # SQLite database
└── README.md               # This file
```

## Database Models

### Patient
- First Name
- Last Name
- Date of Birth
- Gender
- Phone
- Address

### Doctor
- First Name
- Last Name
- Specialization
- Phone
- Email

### Appointment
- Patient (Foreign Key)
- Doctor (Foreign Key)
- Appointment Date & Time
- Reason
- **Constraints**: Prevents duplicate appointments for same patient/doctor at the same time

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd c:\DDU\Sem4\SP\HMS
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Or install Django:
   ```bash
   pip install Django==6.0.2
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Public Home: http://localhost:8000/
   - Admin Panel: http://localhost:8000/admin/
   - Dashboard: http://localhost:8000/dashboard/
   - Patients: http://localhost:8000/patients/
   - Doctors: http://localhost:8000/doctors/
   - Appointments: http://localhost:8000/appointments/

## URL Routes

| Route | Description |
|-------|-------------|
| `/` | Public home page |
| `/login/` | User login |
| `/logout/` | User logout |
| `/dashboard/` | Dashboard (authenticated users) |
| `/admin/` | Django admin panel |
| `/patients/` | Patient list and management |
| `/doctors/` | Doctor list and management |
| `/appointments/` | Appointment list and booking |

## Key Features

### Appointment Validation
- Prevents a doctor from having multiple appointments at the same time
- Prevents a patient from having multiple appointments at the same time
- Enforces these constraints at both model and database level

### Authentication
- Login required for accessing dashboard and management features
- Secure logout functionality
- Customizable login view

### Admin Interface
- Full Django admin support
- Easy management of all entities
- Built-in user and permission system

## Technologies Used

- **Framework**: Django 6.0.2
- **Database**: SQLite3
- **Frontend**: HTML/CSS/JavaScript (templates)
- **Backend**: Python 3

## Development Notes

- The project uses Django's built-in authentication system
- SQLite is used for development (consider PostgreSQL for production)
- DEBUG mode is enabled (disable for production)
- SECRET_KEY in settings.py should be kept secret in production

## License

This project is created as part of coursework.

## Author

Created for HMS (Hospital Management System) project - Semester 4, Software Project (SP)
