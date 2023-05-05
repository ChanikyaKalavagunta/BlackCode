from rest_framework import serializers
from .models import OTP

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ('email', 'phone_number', 'otp', 'created_at', 'is_used')
        read_only_fields = ('created_at','is_used')