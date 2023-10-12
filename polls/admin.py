from django.contrib import admin

from . import models


class ChoiceInline(admin.TabularInline):
    model = models.Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"],
                              "classes": ["collapse"]}),
    )
    inlines = [ChoiceInline]
    list_display = (
        "question_text",
        "pub_date",
        "was_published_recently",
    )
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


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


class RegistrationCodeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'phone',
        'code',
        'time_create'
    )
    list_display_links = (
        'id',
        'phone',
        'code'
    )
    fields = (
        'phone',
        'code',
        'time_create'
    )
    readonly_fields = (
        'code',
        'time_create',
    )


admin.site.register(models.Question, QuestionAdmin)
# admin.site.register(models.Choice, ChoiceAdmin)
admin.site.register(models.RegistrationCode, RegistrationCodeAdmin)