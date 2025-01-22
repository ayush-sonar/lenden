from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, GameHistoryView , GameHistoryDetailView

router = DefaultRouter()
router.register(r'', GameViewSet, basename='game')

urlpatterns = [
    path('history/', GameHistoryView.as_view(), name='game-history'),
    path('history/<uuid:pk>/', GameHistoryDetailView.as_view(), name='game-history-detail'),
] + router.urls