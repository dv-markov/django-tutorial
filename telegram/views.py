
from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import RegistrationCode, TelegramId
from .serializers import (
    GenerateCodeSerializer,
    VerifyCodeSerializer,
)
from . import services


class GenerateCodeView(generics.CreateAPIView):
    serializer_class = GenerateCodeSerializer


class VerifyCodeView(generics.CreateAPIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        try:
            if request.data.get('tg-bot-token') != settings.TG_BOT_TOKEN:
                return Response({'detail': 'Доступ запрещен'}, status=status.HTTP_403_FORBIDDEN)
            code = request.data.get('code')
            reg_code_object = RegistrationCode.objects.filter(code=code)
            phone = reg_code_object.values('phone').last()['phone']
        except Exception as e:
            response_data = {'status': 'Введенный код не найден, пройдите регистрацию на сайте realworker.ru',
                             # 'detail': f'Ошибка: {e}',
                             'authorized': False}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        telegram_id_object = TelegramId.objects.filter(phone=phone)
        if telegram_id_object.exists():
            # telegram_id = telegram_id_object.last()
            # serializer = self.get_serializer(telegram_id)
            response_data = {'status': f'Номер {phone} уже есть в базе',
                             'authorized': True}
            # response_data.update(serializer.data)
            response_status = status.HTTP_200_OK
        else:
            request_data = request.data.copy()
            request_data.update({'phone': phone})

            serializer = self.get_serializer(
                data=request_data,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            response_data = {'status': f'Номер {phone} успешно прошел верификацию',
                             'authorized': True}
            response_status = status.HTTP_201_CREATED

        services.delete_expired_codes(phone)

        return Response(response_data, status=response_status)

