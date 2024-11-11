from django.contrib import admin
from info import models as info_models


@admin.register(info_models.PartnerRequest)
class PartnerRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'city', 'submitted_at')
    list_filter = ('submitted_at', 'city')
    search_fields = ('name', 'email', 'phone', 'city', 'description')
    readonly_fields = ('name', 'phone_code', 'phone', 'email', 'city', 'description', 'submitted_at')

    def has_add_permission(self, request):
        return False


@admin.register(info_models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'topic', 'message')
    search_fields = ('username', 'email', 'topic')
    list_filter = ('topic',)
