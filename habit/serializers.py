from rest_framework import serializers
from .models import Habit,DailyRecord

class DailyRecordSerializer(serializers.ModelSerializer):
    target = serializers.IntegerField(source='habit.target',read_only=True)
    unit = serializers.CharField(source = 'habit.unit',read_only=True)

    class Meta:
        model = DailyRecord
        fields = [
            'id',
            'habit',
            'date',
            'amount_achieved',
            'target',
            'unit',
        ]
        read_only_fields = ('id',)

class HabitSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    daily_records = DailyRecordSerializer(many=True,read_only=True)

    class Meta:
        model = Habit
        fields = [
            'id',
            'user',
            'name',
            'description',
            'target',
            'unit',
            'daily_records',
        ]
        read_only_fields = ('id','user') 
