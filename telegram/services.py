import random
import datetime

from django.utils import timezone
from django.db.models import Q

from . import models


def generate_code():
    return random.randint(100000, 999999)


def delete_expired_codes(phone):
    now = timezone.now()
    expired_codes_time = now - datetime.timedelta(minutes=5)
    deletion_report = models.RegistrationCode.objects.filter(
        Q(phone=phone) | Q(time_create__lte=expired_codes_time)
    ).delete()
