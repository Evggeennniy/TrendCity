from django.contrib import admin
from django.urls import include, path
from info import views as info_views

urlpatterns = [
    path('aboutus/', info_views.AboutUsView.as_view(), name='about_us'),
    path('partner-form/', info_views.partner_form_view, name='partner_form'),
    path('contacts/', info_views.ContactsView.as_view(), name='contacts'),
    path('feedback/', info_views.feedback_form_view, name='feedback_form'),
    path('privacy-policy/', info_views.PrivacyPolicyView.as_view(), name='privacypolicy'),
    path('public-offer-agreement/', info_views.PublicOfferАgreementView.as_view(), name='publicofferagreement'),
]
