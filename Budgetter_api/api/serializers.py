from rest_framework import serializers
from .models import Payment, PaymentDetail, PurchaseCategory, PaymentRecord, PaymentGroup

class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = ['id', 'name', 'is_active', 'payment']

class PaymentSerializer(serializers.ModelSerializer):
    details = PaymentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'name', 'is_active', 'details']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class PurchaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseCategory
        fields = ['id', 'name', 'is_active']

class PaymentRecordSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    payment_detail = PaymentDetailSerializer(read_only=True)
    category = PurchaseCategorySerializer(read_only=True)
    
    payment_id =  serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all(), write_only=True)
    payment_detail_id = serializers.PrimaryKeyRelatedField(queryset=PaymentDetail.objects.all(), write_only=True, required=False, allow_null=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=PurchaseCategory.objects.all(), write_only=True)

    class Meta:
        model = PaymentRecord
        fields = ['id', 'name', 'date', 'price', 'payment', 'payment_detail', 'category', 'payment_id', 'payment_detail_id', 'category_id']

    def create(self, validated_date):
        validated_date['payment'] = validated_date.get('payment_id', None)
        validated_date['payment_detail'] = validated_date.get('payment_detail_id', None)
        validated_date['category'] = validated_date.get('category_id', None)

        del validated_date['payment_id']
        del validated_date['payment_detail_id']
        del validated_date['category_id']

        return PaymentRecord.objects.create(**validated_date)

class PaymentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGroup
        fields = ['id', 'name', 'payments', 'payment_details', 'order', 'is_active']