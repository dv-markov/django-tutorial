from django.contrib import admin

from . import models


class ChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'question',
        'choice_text',
        'votes',
    )
    list_display_links = (
        'id',
        'question',
        'choice_text',
    )


admin.site.register(models.Question)
admin.site.register(models.Choice, ChoiceAdmin)
