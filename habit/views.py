from django.db.models import Prefetch, Avg, Max,Sum
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Habit,DailyRecord
from .serializers import HabitSerializer,DailyRecordSerializer
from .permissions import IsOwner

class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated,IsOwner]

    def get_queryset(self):
        daily_records_prefetch = Prefetch(
            'daily_records',
            queryset=DailyRecord.objects.only('id', 'date', 'amount_achieved',),
            to_attr='prefetched_daily_records'
        )
        return Habit.objects.filter(user=self.request.user).prefetch_related(daily_records_prefetch).annotate(
            average = Avg('daily_records__amount_achieved'),
            total = Sum(('daily_records__amount_achieved')),
            best = Max(('daily_records__amount_achieved'))
        )

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class DailyRecordViewSet(viewsets.ModelViewSet):
    serializer_class = DailyRecordSerializer
    permission_classes = [IsAuthenticated,IsOwner]

    def perform_create(self, serializer):
        habit = serializer.validated_data['habit']
        if habit.user != self.request.user:
            raise PermissionDenied("You can only create records for your own habits.")
        serializer.save()

    def get_queryset(self):
        return DailyRecord.objects.filter(habit__user=self.request.user).select_related('habit')





