from rest_framework import routers
from .views import HabitViewSet,DailyRecordViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register('habits',HabitViewSet,basename='habit')
router.register('daily-records',DailyRecordViewSet,basename='dailyrecord')

urlpatterns = router.urls