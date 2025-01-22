from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, GameHistoryView

router = DefaultRouter()
router.register(r'', GameViewSet, basename='game')

urlpatterns = [
    path('history/', GameHistoryView.as_view(), name='game-history'),
] + router.urls