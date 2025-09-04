from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Habit,DailyRecord
from .serializers import HabitSerializer,DailyRecordSerializer
from .permissions import IsOwner

class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated,IsOwner]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).prefetch_related('daily_records')

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class DailyRecordViewSet(viewsets.ModelViewSet):
    serializer_class = DailyRecordSerializer
    permission_classes = [IsAuthenticated,IsOwner]

    def get_queryset(self):
        return DailyRecord.objects.filter(habit__user=self.request.user).select_related('habit')





