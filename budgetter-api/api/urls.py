from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    get_current_user,
    PasswordChangeAPIView,
    PaymentViewSet,
    PaymentDetailViewSet,
    CategoryViewSet,
    CategoryDetailViewSet,
    PaymentRecordViewSet,
    SubscriptionViewSet,
    LoanRecordViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)
router.register(r'payment-details', PaymentDetailViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'category-details', CategoryDetailViewSet)
router.register(r'records', PaymentRecordViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'loans', LoanRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('me', get_current_user),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-change/', PasswordChangeAPIView.as_view(), name='password_change'),
]
