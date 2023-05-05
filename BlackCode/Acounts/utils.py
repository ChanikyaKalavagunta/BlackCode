from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail

import random

User = get_user_model()

def generate_otp():
    """
    Generate a random OTP.
    """
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    """
    Send the OTP to the given email address.
    """
    subject = _('Your OTP for verification')
    message = _('Your OTP for verification is {otp}. This OTP is valid for 10 minutes.').format(otp=otp)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
# utils.py

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

import random
import smtplib
from email.mime.text import MIMEText

User = get_user_model()

def generate_otp():
    """
    Generate a random OTP.
    """
    return random.randint(100000, 999999)

def send_otp_sms(phone_number, otp):
    """
    Send the OTP via SMS.
    """
    # TODO: Replace with your SMS API integration
    # For example, you can use the Twilio API or any other SMS API provider.
    # Here, we'll send the OTP via email instead of SMS.
    
    message = f"Your OTP is: {otp}"
    
    # Construct the email message
    msg = MIMEText(message)
    msg['From'] = settings.DEFAULT_FROM_EMAIL
    msg['To'] = phone_number
    msg['Subject'] = 'OTP Verification'
    
    # Send the email message via SMTP
    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as smtp:
            smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            smtp.sendmail(settings.DEFAULT_FROM_EMAIL, phone_number, msg.as_string())
    except Exception as e:
        print(f"Failed to send OTP via email: {e}")
        # TODO: Handle the exception appropriately