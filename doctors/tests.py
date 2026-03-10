from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from appointments.models import Appointment, AppointmentDocument
from patients.models import Patient
from .models import Doctor
import io


class DoctorHistoryTests(TestCase):
    def setUp(self):
        # create doctor group
        self.doctor_group, _ = Group.objects.get_or_create(name='Doctor')
        # user and doctor profile
        self.user = User.objects.create_user(username='doc1', password='pass')
        self.user.groups.add(self.doctor_group)
        self.doctor = Doctor.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            specialization='General',
            phone='123456',
            email='doc@example.com'
        )
        # a patient
        self.patient = Patient.objects.create(
            first_name='Jane',
            last_name='Smith',
            date_of_birth='1990-01-01',
            gender='Female',
            phone='987654',
            address='123 Main St'
        )
        # a past appointment
        self.appt = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now() - timezone.timedelta(days=1),
            reason='Checkup'
        )
        self.client = Client()

    def test_doctor_can_register_and_login(self):
        # create a doctor record without linked user
        doc = Doctor.objects.create(
            first_name='Alice',
            last_name='Wonder',
            specialization='Cardiology',
            phone='555-0000',
            email='alice@example.com'
        )
        response = self.client.post('/doctors/register/', {
            'email': 'alice@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        })
        self.assertEqual(response.status_code, 302)
        # login with new credentials
        login_ok = self.client.login(username='alice@example.com', password='complexpass123')
        self.assertTrue(login_ok)
        # check doctor profile linked
        doc.refresh_from_db()
        self.assertIsNotNone(doc.user)
        # newly created user should have first/last name copied
        self.assertEqual(doc.user.first_name, 'Alice')
        self.assertEqual(doc.user.last_name, 'Wonder')
        # newly created user should be in Doctor group
        self.assertTrue(doc.user.groups.filter(name='Doctor').exists())

    def test_registration_reuses_existing_user(self):
        doc2 = Doctor.objects.create(
            first_name='Bob',
            last_name='Builder',
            specialization='Surgery',
            phone='555-1111',
            email='bob@example.com'
        )
        existing = User.objects.create_user(username='bob@example.com', email='bob@example.com', password='oldpass')
        # perform registration, should update password and link
        response = self.client.post('/doctors/register/', {
            'email': 'bob@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
        })
        self.assertEqual(response.status_code, 302)
        doc2.refresh_from_db()
        self.assertEqual(doc2.user, existing)
        # refresh the user instance from database before checking password
        existing.refresh_from_db()
        self.assertTrue(existing.check_password('newpass123'))

    def test_history_page_shows_appointment(self):
        self.client.login(username='doc1', password='pass')
        response = self.client.get('/doctors/history/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Checkup')
        self.assertContains(response, 'Jane Smith')

    def test_string_representation_uses_model_name_when_user_missing(self):
        # doctor with user but the user has no first/last; __str__ should fallback
        user = User.objects.create_user(username='nopname', password='x')
        doc = Doctor.objects.create(
            user=user,
            first_name='Empty',
            last_name='Name',
            specialization='Test',
            phone='123',
            email='empty@example.com'
        )
        # user has blank full name by default
        self.assertEqual(str(doc), 'Dr. Empty Name')

    def test_upload_document_creates_record(self):
        self.client.login(username='doc1', password='pass')
        upload = SimpleUploadedFile('test.txt', b"dummy content")
        response = self.client.post('/doctors/history/', {
            'appointment_id': self.appt.id,
            'file': upload,
            'description': 'Prescription'
        })
        self.assertEqual(response.status_code, 302)  # redirected
        docs = AppointmentDocument.objects.filter(appointment=self.appt)
        self.assertEqual(docs.count(), 1)
        self.assertEqual(docs.first().description, 'Prescription')
