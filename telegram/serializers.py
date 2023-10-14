import datetime

from django.utils import timezone
from rest_framework import serializers

from .models import RegistrationCode, TelegramId


class GenerateCodeSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        validators=[RegistrationCode.phone_regex],
        max_length=16,
        write_only=True
    )
    code = serializers.IntegerField(read_only=True)

    class Meta:
        model = RegistrationCode
        fields = [
            'phone',
            'code',
        ]

    @staticmethod
    def __was_created_recently(reg_code_time_create: datetime.datetime) -> bool:
        now = timezone.now()
        return now - datetime.timedelta(minutes=1) <= reg_code_time_create <= now

    def validate(self, attrs):
        phone = attrs.get('phone')
        current_phone_in_db = RegistrationCode.objects.filter(phone=phone)
        if current_phone_in_db.exists():
            reg_code_object = current_phone_in_db.values('code', 'phone', 'time_create').last()
            time_create = reg_code_object['time_create']
            if self.__was_created_recently(time_create):
                code = reg_code_object['code']
                phone = reg_code_object['phone']
                time_delta = timezone.now() - time_create
                time_left = datetime.timedelta(minutes=1) - time_delta
                time_left_seconds = time_left.seconds
                raise serializers.ValidationError(f"Текущий код {code} для телефона {phone} активен."
                                                  f"Новый код может быть сгенерирован через {time_left_seconds} секунд")
            current_phone_in_db.delete()

        return attrs


class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=16)
    telegram_id = serializers.CharField(max_length=15)
    telegram_name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return TelegramId.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


# class VerifyCodeSerializer2(serializers.ModelSerializer):
#     phone = serializers.SerializerMethodField()
#     # phone = serializers.CharField(allow_blank=True)
#
#     class Meta:
#         model = TelegramId
#         fields = "__all__"
#
#     def get_phone(self, obj):
#         return self.context['phone']
