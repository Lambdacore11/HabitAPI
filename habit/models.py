from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='habits',on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    target = models.IntegerField(validators=[MinValueValidator(1)])
    unit = models.CharField(max_length=20)
    success = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.name} {self.user.username}'

class DailyRecord(models.Model):
    habit = models.ForeignKey(Habit,related_name='daily_records',on_delete=models.CASCADE)
    date = models.DateField()
    amount_achieved = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.habit.name} on {self.date}: {self.amount_achieved}/{self.habit.target}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['habit','date'],
                name = 'unique_daily_record',
            )
        ]

