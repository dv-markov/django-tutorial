from django.contrib import admin
from . import models


class RegistrationCodeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'phone',
        'code',
        'time_create',
    )
    list_display_links = (
        'id',
        'phone',
    )
    fields = (
        'phone',
        'code',
        'time_create',
    )
    readonly_fields = (
        'code',
        'time_create',
    )


class TelegramIdAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'phone',
        'telegram_id',
        'telegram_name',
        'user',
        'time_create',
        'time_update',
    )
    list_display_links = (
        'id',
        'phone',
        'telegram_id',
    )
    fields = (
        'phone',
        'telegram_id',
        'telegram_name',
        'user',
        'time_create',
        'time_update',
    )
    readonly_fields = (
        'time_create',
        'time_update',
    )


admin.site.register(models.RegistrationCode, RegistrationCodeAdmin)
admin.site.register(models.TelegramId, TelegramIdAdmin)
