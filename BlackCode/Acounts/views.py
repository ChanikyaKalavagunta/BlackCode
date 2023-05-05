# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.core.exceptions import ValidationError
# from django.core.validators import validate_email
# from .models import OTP
# from .utils import generate_otp, send_otp_email, send_otp_sms
# import phonenumbers
# @api_view(['POST'])
# def send_otp(request):
#     email_or_phone = request.data.get('email_or_phone')
#     if not email_or_phone:
#         return Response({'error': 'Email or phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
    
#     # Validate the email or phone number
#     try:
#         validate_email(email_or_phone)
#         otp_obj = OTP.objects.create(email=email_or_phone, otp=generate_otp())
#         send_otp_email(email_or_phone, otp_obj.otp)
#     except ValidationError:
#         otp_obj = OTP.objects.create(phone_number=email_or_phone, otp=generate_otp())
#         send_otp_sms(email_or_phone, otp_obj.otp)
    
#     otp_obj.save()
#     return Response({'message': 'OTP sent successfully'})

# @api_view(['PUT'])
# def verify_otp(request):
#     email_or_phone = request.data.get('email_or_phone')
#     otp = request.data.get('otp')
    
#     # Check if the OTP exists in the database
#     try:
#         otp_obj = OTP.objects.get(email=email_or_phone, otp=otp)
#     except OTP.DoesNotExist:
#         try:
#             otp_obj = OTP.objects.get(phone_number=email_or_phone, otp=otp)
#         except OTP.DoesNotExist:
#             return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
    
#     # Check if the OTP is expired
#     if otp_obj.is_expired():
#         return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
    
#     # Mark the OTP as used
#     otp_obj.is_used = True
#     otp_obj.save()
    
#     return Response({'message': 'OTP verifiedsuccessfully'})

import phonenumbers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import OTP
from .utils import generate_otp, send_otp_email, send_otp_sms

@api_view(['POST'])
def send_otp(request):
    email_or_phone = request.data.get('email_or_phone')
    if not email_or_phone:
        return Response({'error': 'Email or phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
    # Validate the email or phone number
    try:
        validate_email(email_or_phone)
        otp_obj = OTP.objects.create(email=email_or_phone, otp=generate_otp())
        send_otp_email(email_or_phone, otp_obj.otp)
    except ValidationError:
        try:
            # Parse the phone number using the default region of "US"
            parsed_number = phonenumbers.parse(email_or_phone, "US")

            # If the phone number is valid, format it in E.164 format
            if phonenumbers.is_valid_number(parsed_number):
                phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

                # Create the OTP object with the formatted phone number
                otp_obj = OTP.objects.create(phone_number=phone_number, otp=generate_otp())
                send_otp_sms(phone_number, otp_obj.otp)
            else:
                # If the phone number is not valid, raise a validation error
                raise ValidationError("Invalid phone number")
        except phonenumbers.NumberParseException:
            # If the phone number is not parseable, raise a validation error
            raise ValidationError("Invalid phone number")
    
    otp_obj.save()
    return Response({'message': 'OTP sent successfully'})
