import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.core.validators import RegexValidator

from . import services


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?"
    )
    def was_published_recently(self) -> bool:
        now = timezone.now()
        return now - datetime.timedelta(minutes=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class RegistrationCode(models.Model):
    # phone = models.PositiveIntegerField(db_index=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?\d{8,15}$',
                                 message="Phone number must be entered in the format: '+79876543210'. "
                                         "Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=16)
    code = models.PositiveIntegerField(null=True)
    time_create = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = services.generate_code()
        super().save(*args, **kwargs)
