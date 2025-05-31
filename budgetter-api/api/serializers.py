from rest_framework import serializers
from .models import (
    Payment, 
    PaymentDetail, 
    Category, 
    CategoryDetail, 
    PaymentRecord, 
    Subscription,
    LoanRecord
)

class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = ['id', 'name', 'is_active', 'payment', 'order']

class PaymentSerializer(serializers.ModelSerializer):
    details = PaymentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'name', 'is_active', 'details', 'icon', 'order']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryDetail
        fields = ['id', 'name', 'is_active', 'category', 'order']

class CategorySerializer(serializers.ModelSerializer):
    details = CategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'is_active', 'details', 'icon', 'order']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class PaymentRecordSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    payment_detail = PaymentDetailSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_detail = CategoryDetailSerializer(read_only=True)
    
    payment_id =  serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all(), write_only=True)
    payment_detail_id = serializers.PrimaryKeyRelatedField(queryset=PaymentDetail.objects.all(), write_only=True, required=False, allow_null=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    category_detail_id = serializers.PrimaryKeyRelatedField(queryset=CategoryDetail.objects.all(), write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = PaymentRecord
        fields = ['id', 'name', 'date', 'price', 'is_active', 'payment', 'payment_detail', 'category', 'category_detail', 'payment_id', 'payment_detail_id', 'category_id', 'category_detail_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['payment_id'].queryset = Payment.objects.filter(user=user, is_active=True)
        self.fields['payment_detail_id'].queryset = PaymentDetail.objects.filter(payment__user=user, is_active=True)
        self.fields['category_id'].queryset = Category.objects.filter(user=user, is_active=True)
        self.fields['category_detail_id'].queryset = CategoryDetail.objects.filter(category__user=user, is_active=True)

    def create(self, validated_data):
        validated_data['payment'] = validated_data.pop('payment_id', None)
        validated_data['payment_detail'] = validated_data.pop('payment_detail_id', None)
        validated_data['category'] = validated_data.pop('category_id', None)
        validated_data['category_detail'] = validated_data.pop('category_detail_id', None)
        validated_data['user'] = self.context['request'].user
        return PaymentRecord.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field in ['payment_id', 'payment_detail_id', 'category_id', 'category_detail_id']:
            validated_data.pop(field, None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class SubscriptionSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    payment_detail = PaymentDetailSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_detail = CategoryDetailSerializer(read_only=True)
    
    payment_id =  serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all(), write_only=True)
    payment_detail_id = serializers.PrimaryKeyRelatedField(queryset=PaymentDetail.objects.all(), write_only=True, required=False, allow_null=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    category_detail_id = serializers.PrimaryKeyRelatedField(queryset=CategoryDetail.objects.all(), write_only=True, required=False, allow_null=True)

    class Meta:
        model = Subscription
        fields = ['id', 'name', 'price', 'is_active', 'payment', 'payment_detail', 'category', 'category_detail', 'payment_id', 'payment_detail_id', 'category_id', 'category_detail_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['payment_id'].queryset = Payment.objects.filter(user=user, is_active=True)
        self.fields['payment_detail_id'].queryset = PaymentDetail.objects.filter(payment__user=user, is_active=True)
        self.fields['category_id'].queryset = Category.objects.filter(user=user, is_active=True)
        self.fields['category_detail_id'].queryset = CategoryDetail.objects.filter(category__user=user, is_active=True)

    def create(self, validated_data):
        validated_data['payment'] = validated_data.pop('payment_id', None)
        validated_data['payment_detail'] = validated_data.pop('payment_detail_id', None)
        validated_data['category'] = validated_data.pop('category_id', None)
        validated_data['category_detail'] = validated_data.pop('category_detail_id', None)
        validated_data['user'] = self.context['request'].user
        return Subscription.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field in ['payment_id', 'payment_detail_id', 'category_id', 'category_detail_id']:
            validated_data.pop(field, None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class LoanRecordSerializer(serializers.ModelSerializer):
    loan_type_display = serializers.CharField(source='get_loan_type_display', read_only=True)

    class Meta:
        model = LoanRecord
        fields = ['id', 'name', 'date', 'price', 'loan_type', 'loan_type_display', 'detail', 'is_active']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return LoanRecord.objects.create(**validated_data)
