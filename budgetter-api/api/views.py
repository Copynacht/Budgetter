import datetime
from django.db.models import Prefetch, Sum
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import status, views, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Payment, PaymentDetail, Category, CategoryDetail, PaymentRecord, Subscription, LoanRecord
from .serializers import (
    PaymentSerializer, 
    PaymentDetailSerializer, 
    CategorySerializer, 
    CategoryDetailSerializer, 
    PaymentRecordSerializer, 
    SubscriptionSerializer,
    LoanRecordSerializer
)
from .filters import PaymentRecordFilter


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
    })

class PasswordChangeAPIView(views.APIView):
    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')

        if not current_password or not new_password or not new_password_confirm:
            return Response({'error': 'すべてのパスワードを入力してください'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != new_password_confirm:
            return Response({'error': '新しいパスワードと確認用パスワードが一致しません'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(current_password):
            return Response({'error': '現在のパスワードが間違っています'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'パスワードを変更しました'}, status=status.HTTP_200_OK)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    http_method_names = ['get', 'post', 'put', 'patch']

    def get_queryset(self):
        user = self.request.user
        details_qs = PaymentDetail.objects.filter(
            is_active=True,
            payment__user=user
        ).order_by('order')

        return Payment.objects.filter(user=user, is_active=True).order_by('order') \
            .prefetch_related(Prefetch('details', queryset=details_qs))

    # ユニークフィールドで参照するためis_activeは必須
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        if 'is_active' not in data:
            data['is_active'] = instance.is_active

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

class PaymentDetailViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'put', 'patch']
    queryset = PaymentDetail.objects.all()
    serializer_class = PaymentDetailSerializer
    
    # ユニークフィールドで参照するためis_activeは必須
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        if 'is_active' not in data:
            data['is_active'] = instance.is_active

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    ordering = ['-order']
    
    def get_queryset(self):
        user = self.request.user
        details_qs = CategoryDetail.objects.filter(
            is_active=True,
            category__user=user
        ).order_by('order')

        return Category.objects.filter(user=user, is_active=True).order_by('order') \
            .prefetch_related(Prefetch('details', queryset=details_qs))

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        if 'is_active' not in data:
            data['is_active'] = instance.is_active

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryDetailViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'put', 'patch']
    queryset = CategoryDetail.objects.all()
    serializer_class = CategoryDetailSerializer
    
    # ユニークフィールドで参照するためis_activeは必須
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        if 'is_active' not in data:
            data['is_active'] = instance.is_active

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

class PaymentRecordViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch']
    queryset = PaymentRecord.objects.all()
    serializer_class = PaymentRecordSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentRecordFilter
    ordering_fields = ['price', 'date']
    ordering = ['-date', '-id']

    def get_queryset(self):
        user = self.request.user
        return PaymentRecord.objects.filter(user=user, is_active=True) \
            .select_related('payment', 'payment_detail', 'category', 'category_detail')

    @extend_schema(
        parameters=[
            OpenApiParameter(name='year', required=True, type=int, description='対象の年'),
            OpenApiParameter(name='month', required=True, type=int, description='対象の月（0なら年間合計）'),
            OpenApiParameter(name='payment', required=False, type=int, description='PaymentのIDでフィルター'),
            OpenApiParameter(name='payment_detail', required=False, type=int, description='PaymentDetailのIDでフィルター'),
            OpenApiParameter(name='category', required=False, type=int, description='CategoryのIDでフィルター'),
            OpenApiParameter(name='category_detail', required=False, type=int, description='CategoryDetailのIDでフィルター'),
        ],
        responses={200: OpenApiTypes.OBJECT}
    )
    @action(detail=False, methods=['get'], url_path='sum-by-month')
    def sum_by_month(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if not year or not month:
            return Response({'error': 'year and month are required parameters.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response({'error': 'year and month must be integers.'},
                            status=status.HTTP_400_BAD_REQUEST)

        payment = request.query_params.get('payment')
        payment_detail = request.query_params.get('payment_detail')
        category = request.query_params.get('category')
        category_detail = request.query_params.get('category_detail')

        # 日付範囲の決定
        if month == 0:
            start_date = datetime.date(year, 1, 1)
            end_date = datetime.date(year + 1, 1, 1)
        elif 1 <= month <= 12:
            start_date = datetime.date(year, month, 1)
            if month == 12:
                end_date = datetime.date(year + 1, 1, 1)
            else:
                end_date = datetime.date(year, month + 1, 1)
        else:
            return Response({'error': 'month must be between 0 and 12.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # ベースのクエリセット（ユーザーとアクティブ判定含む）
        queryset = self.get_queryset().filter(date__gte=start_date, date__lt=end_date)

        # optionalフィルターを追加
        if payment is not None:
            try:
                payment_id = int(payment)
                queryset = queryset.filter(payment_id=payment_id)
            except ValueError:
                return Response({'error': 'payment must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

        if payment_detail is not None:
            try:
                payment_detail_id = int(payment_detail)
                queryset = queryset.filter(payment_detail_id=payment_detail_id)
            except ValueError:
                return Response({'error': 'payment_detail must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

        if category is not None:
            try:
                category_id = int(category)
                queryset = queryset.filter(category_id=category_id)
            except ValueError:
                return Response({'error': 'category must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

        if category_detail is not None:
            try:
                category_detail_id = int(category_detail)
                queryset = queryset.filter(category_detail_id=category_detail_id)
            except ValueError:
                return Response({'error': 'category_detail must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = queryset.aggregate(total=Sum('price'))['total'] or 0

        return Response({'year': year, 'month': month, 'total_price': total_price})

class SubscriptionViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch']
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    ordering = ['-id']

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(user=user, is_active=True)

    @action(detail=False, methods=['get'], url_path='sum-all-prices')
    def sum_all_prices(self, request):
        total_price = self.get_queryset().aggregate(total=Sum('price'))['total'] or 0
        return Response({'total_price': total_price}, status=status.HTTP_200_OK)

class LoanRecordViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch']
    queryset = LoanRecord.objects.all()
    serializer_class = LoanRecordSerializer

    def get_queryset(self):
        user = self.request.user
        return LoanRecord.objects.filter(user=user, is_active=True)
