from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import DailyRecord

@receiver(post_save, sender=DailyRecord)
def update_habit_success_on_save(sender, instance, created, **kwargs):
    habit = instance.habit
    has_success = habit.daily_records.filter(amount_achieved__gte=habit.target).exists()
    
    if habit.success != has_success:
        habit.success = has_success
        habit.save(update_fields=['success'])

@receiver(post_delete, sender=DailyRecord)
def update_habit_success_on_delete(sender, instance, **kwargs):
    habit = instance.habit
    has_success = habit.daily_records.filter(amount_achieved__gte=habit.target).exists()
    
    if habit.success != has_success:
        habit.success = has_success
        habit.save(update_fields=['success'])