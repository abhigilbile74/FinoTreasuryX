from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import GoalViewSet, ContributionViewSet, StrategyItemViewSet
from rest_framework.authtoken import views as drf_views

router = DefaultRouter()
router.register(r'goals', GoalViewSet, basename='goal')
router.register(r'contributions', ContributionViewSet, basename='contribution')
router.register(r'strategy', StrategyItemViewSet, basename='strategy')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', drf_views.obtain_auth_token, name='api-token'),  # POST username & password => token
]
