from django.db import models
from django.core.validators import RegexValidator

from base.models import BaseStrIdModel
from apps.users.models import CustomUser
from . import services


class RegistrationCode(models.Model):
    # phone = models.PositiveIntegerField(db_index=True, null=True)
    phone_regex = RegexValidator(regex=r'^\d{8,15}$',
                                 message="Телефонный номер необходимо ввести в формате: '79876543210'.")
    phone = models.CharField(validators=[phone_regex], max_length=15)
    code = models.PositiveIntegerField(null=True)
    time_create = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = services.generate_code()
        super().save(*args, **kwargs)


class TelegramId(BaseStrIdModel):
    phone = models.CharField(max_length=16, db_index=True, unique=True)
    telegram_id = models.CharField(max_length=15)
    telegram_name = models.CharField(max_length=100)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )




