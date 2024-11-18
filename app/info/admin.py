from django.contrib import admin
from info import models as info_models
from django.utils.html import strip_tags


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


@admin.register(info_models.PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('display_text',)
    search_fields = ()
    list_filter = ()

    def display_text(self, obj):
        return strip_tags(obj.text)


@admin.register(info_models.PublicOfferАgreement)
class PublicOfferАgreementAdmin(admin.ModelAdmin):
    list_display = ('display_text',)
    search_fields = ()
    list_filter = ()

    def display_text(self, obj):
        return strip_tags(obj.text)


@admin.register(info_models.AboutUsHeader)
class AboutUsHeaderAdmin(admin.ModelAdmin):
    list_display = ('display_text',)
    search_fields = ()
    list_filter = ()

    def display_text(self, obj):
        return strip_tags(obj.text)


@admin.register(info_models.AboutUsForClients)
class AboutUsForClientsAdmin(admin.ModelAdmin):
    list_display = ('header', 'display_text',)
    search_fields = ()
    list_filter = ()

    def display_text(self, obj):
        return strip_tags(obj.text)


@admin.register(info_models.AboutUsForm)
class AboutUsFormAdmin(admin.ModelAdmin):
    list_display = ('display_text',)
    search_fields = ()
    list_filter = ()

    def display_text(self, obj):
        return strip_tags(obj.text)


@admin.register(info_models.AboutUsReview)
class AboutUsReviewAdmin(admin.ModelAdmin):
    list_display = ('grade', 'display_text', 'name')
    search_fields = ()
    list_filter = ()

    def display_text(self, obj):
        return strip_tags(obj.text)


@admin.register(info_models.ContactText)
class ContactTextAdmin(admin.ModelAdmin):
    list_display = ('header', 'value')
    search_fields = ()
    list_filter = ()


@admin.register(info_models.ContactLink)
class ContactLink(admin.ModelAdmin):
    list_display = ('header', 'link')
    search_fields = ()
    list_filter = ()
