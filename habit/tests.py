from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date, timedelta
from .models import Habit, DailyRecord
from .serializers import HabitSerializer, DailyRecordSerializer

User = get_user_model()

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            name='Test Habit',
            description='A test habit',
            target=5,
            unit='times per week'
        )

    def test_habit_creation(self):
        self.assertEqual(self.habit.name, 'Test Habit')
        self.assertEqual(self.habit.user.username, 'testuser')
        self.assertEqual(self.habit.target, 5)

    def test_daily_record_creation(self):
        record = DailyRecord.objects.create(
            habit=self.habit,
            date=date.today(),
            amount_achieved=3
        )
        self.assertEqual(record.habit.name, 'Test Habit')
        self.assertEqual(record.amount_achieved, 3)

    def test_unique_daily_record_constraint(self):
        DailyRecord.objects.create(
            habit=self.habit,
            date=date(2023, 10, 27),
            amount_achieved=2
        )
        
        with self.assertRaises(Exception):
            DailyRecord.objects.create(
                habit=self.habit,
                date=date(2023, 10, 27),
                amount_achieved=4
            )


class ViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        
        self.habit = Habit.objects.create(
            user=self.user,
            name='Reading',
            description='Read 30 minutes daily',
            target=7,
            unit='days per week'
        )
        
        self.record = DailyRecord.objects.create(
            habit=self.habit,
            date=date.today(),
            amount_achieved=1
        )
        
        self.habits_list_url = reverse('habit-list')
        self.habits_detail_url = reverse('habit-detail', kwargs={'pk': self.habit.pk})
        self.records_list_url = reverse('dailyrecord-list')
        self.records_detail_url = reverse('dailyrecord-detail', kwargs={'pk': self.record.pk})

    def test_get_habits_unauthenticated(self):
        response = self.client.get(self.habits_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_habits_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.habits_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Reading')

    def test_create_habit(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Exercise',
            'description': 'Workout daily',
            'target': 5,
            'unit': 'days per week'
        }
        response = self.client.post(self.habits_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Exercise')
        self.assertEqual(response.data['user'], 'testuser') 

    def test_update_own_habit(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Updated Habit'}
        response = self.client.patch(self.habits_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.name, 'Updated Habit')

    def test_cannot_update_other_user_habit(self):
        self.client.force_authenticate(user=self.other_user)
        data = {'name': 'Hacked Habit'}
        response = self.client.patch(self.habits_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_habit(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.habits_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_get_daily_records(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.records_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_daily_record(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'habit': self.habit.pk,
            'date': '2023-10-28',
            'amount_achieved': 1
        }
        response = self.client.post(self.records_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DailyRecord.objects.count(), 2)

    def test_cannot_create_record_for_other_user_habit(self):
        other_habit = Habit.objects.create(
            user=self.other_user,
            name='Other Habit',
            description='Test',
            target=3,
            unit='times'
        )
        
        self.client.force_authenticate(user=self.user)
        data = {
            'habit': other_habit.pk,
            'date': '2023-10-28',
            'amount_achieved': 1
        }
        response = self.client.post(self.records_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_record_validation_less_than_zero(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'habit': self.habit.pk,
            'date': '2023-10-28',
            'amount_achieved': -1
        }
        response = self.client.post(self.records_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unique_record_validation(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'habit': self.habit.pk,
            'date': date.today().isoformat(),
            'amount_achieved': 2
        }
        response = self.client.post(self.records_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SerializerTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            name='Test Habit',
            description='Test',
            target=5,
            unit='times'
        )

    def test_habit_serializer(self):
        """Test habit serializer data"""
        serializer = HabitSerializer(instance=self.habit)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Test Habit')
        self.assertEqual(data['user'], 'testuser')
        self.assertEqual(data['target'], 5)
        self.assertEqual(data['unit'], 'times')

    def test_daily_record_serializer(self):
        """Test daily record serializer with source fields"""
        record = DailyRecord.objects.create(
            habit=self.habit,
            date=date.today(),
            amount_achieved=3
        )
        
        serializer = DailyRecordSerializer(instance=record)
        data = serializer.data
        
        self.assertEqual(data['habit'], self.habit.pk)
        self.assertEqual(data['amount_achieved'], 3)
        self.assertEqual(data['target'], 5)
        self.assertEqual(data['unit'], 'times')

    def test_daily_record_validation(self):
        data = {
            'habit': self.habit.pk,
            'date': '2023-10-27',
            'amount_achieved': -1
        }
        
        serializer = DailyRecordSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('amount_achieved', serializer.errors)


class PermissionTests(TestCase):
    def setUp(self):
        self.factory = APIClient()
        self.user = User.objects.create_user(
            username='owner',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='other',
            password='testpass123'
        )
        
        self.habit = Habit.objects.create(
            user=self.user,
            name='Test Habit',
            description='Test',
            target=5,
            unit='times'
        )
        
        self.record = DailyRecord.objects.create(
            habit=self.habit,
            date=date.today(),
            amount_achieved=3
        )
        
        from .permissions import IsOwner
        self.permission = IsOwner()

    def test_owner_has_permission(self):
        request = self.factory.get('/')
        request.user = self.user
        
        self.assertTrue(self.permission.has_object_permission(request, None, self.habit))
        
        self.assertTrue(self.permission.has_object_permission(request, None, self.record))

    def test_non_owner_no_permission(self):
        request = self.factory.get('/')
        request.user = self.other_user
        
        self.assertFalse(self.permission.has_object_permission(request, None, self.habit))
        
        self.assertFalse(self.permission.has_object_permission(request, None, self.record))

    def test_invalid_object_no_permission(self):
        request = self.factory.get('/')
        request.user = self.user
        
        invalid_obj = object()
        self.assertFalse(self.permission.has_object_permission(request, None, invalid_obj))


class IntegrationTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_complete_workflow(self): 
        habit_data = {
            'name': 'Meditation',
            'description': 'Meditate daily',
            'target': 7,
            'unit': 'days per week'
        }
        response = self.client.post(reverse('habit-list'), habit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        habit_id = response.data['id']
        
        for day in range(3):
            record_data = {
                'habit': habit_id,
                'date': (date.today() - timedelta(days=day)).isoformat(),
                'amount_achieved': 1
            }
            response = self.client.post(reverse('dailyrecord-list'), record_data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.get(reverse('habit-detail', kwargs={'pk': habit_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['daily_records']), 3)
        
        record_id = response.data['daily_records'][0]['id']
        update_data = {'amount_achieved': 2}
        response = self.client.patch(
            reverse('dailyrecord-detail', kwargs={'pk': record_id}),
            update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount_achieved'], 2)