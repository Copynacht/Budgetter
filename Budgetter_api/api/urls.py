from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, PaymentDetailViewSet, PurchaseCategoryViewSet, PaymentRecordViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)
router.register(r'payment-details', PaymentDetailViewSet)
router.register(r'category', PurchaseCategoryViewSet)
router.register(r'record', PaymentRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
