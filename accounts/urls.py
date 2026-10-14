from rest_framework.routers import DefaultRouter
from .views import AccountViewSet

router = DefaultRouter()
router.register('accounts', AccountViewSet, basename='account')

urlpatterns = router.urls

from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import AccountViewSet, StatementView

router = DefaultRouter()
router.register('accounts', AccountViewSet, basename='account')

urlpatterns = router.urls + [
    path('statement/', StatementView.as_view(), name='statement'),
]