import datetime
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from .models import Payment, PaymentDetail, PurchaseCategory, PaymentRecord, PaymentGroup
from .serializers import PaymentSerializer, PaymentDetailSerializer, PurchaseCategorySerializer, PaymentRecordSerializer, PaymentGroupSerializer
from .filters import PaymentRecordFilter


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentDetailViewSet(viewsets.ModelViewSet):
    queryset = PaymentDetail.objects.all()
    serializer_class = PaymentDetailSerializer

class PurchaseCategoryViewSet(viewsets.ModelViewSet):
    queryset = PurchaseCategory.objects.all()
    serializer_class = PurchaseCategorySerializer

class PaymentRecordViewSet(viewsets.ModelViewSet):
    queryset = PaymentRecord.objects.all()
    serializer_class = PaymentRecordSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentRecordFilter
    ordering_fields = ['price', 'date']
    ordering = ['-date']
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='year', required=True, type=int, description='対象の年'),
            OpenApiParameter(name='month', required=True, type=int, description='対象の月（0なら年間合計）')
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

        if month == 0:
            # 年間合計
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

        total_price = PaymentRecord.objects.filter(date__gte=start_date, date__lt=end_date)\
                                        .aggregate(total=Sum('price'))['total'] or 0

        return Response({'year': year, 'month': month, 'total_price': total_price})

class PaymentGroupViewSet(viewsets.ModelViewSet):
    queryset = PaymentGroup.objects.all()
    serializer_class = PaymentGroupSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name='year', required=True, type=int, location=OpenApiParameter.QUERY, description='対象の年'),
            OpenApiParameter(name='month', required=True, type=int, location=OpenApiParameter.QUERY, description='対象の月（0なら年間合計）')
        ],
        responses={200: OpenApiTypes.OBJECT}
    )
    @action(detail=True, methods=['get'], url_path='total-price')
    def total_price(self, request, pk=None):
        group = self.get_object()

        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if not year or not month:
            return Response({"detail": "year and month are required parameters."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response({"detail": "year and month must be integers."}, status=status.HTTP_400_BAD_REQUEST)

        if month == 0:
            start_date = datetime(year, 1, 1).date()
            end_date = datetime(year + 1, 1, 1).date()
        elif 1 <= month <= 12:
            start_date = datetime(year, month, 1).date()
            if month == 12:
                end_date = datetime(year + 1, 1, 1).date()
            else:
                end_date = datetime(year, month + 1, 1).date()
        else:
            return Response({"detail": "month must be between 0 and 12."}, status=status.HTTP_400_BAD_REQUEST)

        records = PaymentRecord.objects.filter(
            date__gte=start_date,
            date__lt=end_date
        ).filter(
            models.Q(payment__in=group.payments.all()) |
            models.Q(payment_detail__in=group.payment_details.all())
        )

        total = records.aggregate(total_price=Sum('price'))['total_price'] or 0

        return Response({"total_price": total})
