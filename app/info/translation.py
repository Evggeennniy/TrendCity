from modeltranslation.translator import register, TranslationOptions
from .models import (
    AboutUsHeader,
    AboutUsForClients,
    AboutUsForm,
    ContactText,
    ContactLink,
    PrivacyPolicy,
    PublicOfferАgreement,
)


@register(AboutUsHeader)
class AboutUsHeaderTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(AboutUsForClients)
class AboutUsForClientsTranslationOptions(TranslationOptions):
    fields = ("header", "text")


@register(AboutUsForm)
class AboutUsFormTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(ContactText)
class ContactTextTranslationOptions(TranslationOptions):
    fields = ("header", "value")


@register(ContactLink)
class ContactLinkTranslationOptions(TranslationOptions):
    fields = ("header", "link")


@register(PrivacyPolicy)
class PrivacyPolicyTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(PublicOfferАgreement)
class PublicOfferАgreementTranslationOptions(TranslationOptions):
    fields = ("text",)
