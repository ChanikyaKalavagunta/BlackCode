from django.db import models
from django.utils import timezone
# Create your models here.


class OTP(models.Model):
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        now = timezone.now()
        return now > self.created_at + timezone.timedelta(minutes=5)