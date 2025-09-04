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
    daily_records = serializers.SerializerMethodField() 
    total = serializers.IntegerField(read_only=True)
    average = serializers.FloatField(read_only=True )
    best = serializers.IntegerField(read_only=True)

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
            'total',
            'average',
            'best',
            'success'
        ]
        read_only_fields = ('id','user') 
    
    def get_daily_records(self, obj):
        records = getattr(obj, 'prefetched_daily_records', None)
        if records is None:
            records = obj.daily_records.only('id', 'date', 'amount_achieved').all()
        return [
            {
                'id': record.id,
                'date': record.date,
                'amount_achieved': record.amount_achieved
            }
            for record in records
        ]
