from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    LogoutView,
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
    path("token/",  CookieTokenObtainPairView.as_view(), name="token_cookie_obtain"),
    path("token/refresh/", CookieTokenRefreshView.as_view(), name="token_cookie_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('password-change/', PasswordChangeAPIView.as_view(), name='password_change'),
]
