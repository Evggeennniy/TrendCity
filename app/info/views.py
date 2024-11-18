from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from catalog.views import PanelView
from django.contrib import messages
from info import models as info_models
from django.http import JsonResponse


class AboutUsView(PanelView, TemplateView):
    template_name = "aboutus.html"


class ContactsView(PanelView, TemplateView):
    template_name = "contacts.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        contact_text_items = info_models.ContactText.objects.all()
        contact_link_items = info_models.ContactLink.objects.all()

        context['contact_text_list'] = contact_text_items
        context['contact_link_list'] = contact_link_items
        return context


class PrivacyPolicyView(PanelView, ListView):
    queryset = info_models.PrivacyPolicy.objects.all()
    template_name = "info_template.html"


class PublicOfferАgreementView(PanelView, ListView):
    queryset = info_models.PublicOfferАgreement.objects.all()
    template_name = "info_template.html"


def partner_form_view(request):
    if request.method == 'POST':
        name = request.POST.get('partners__name')
        phone_code = request.POST.get('partners__phone-code')
        phone = request.POST.get('partners__phone')
        email = request.POST.get('partners__email')
        city = request.POST.get('partners__city')
        description = request.POST.get('partners__text')

        if not all([name, phone_code, phone, email, city, description]):
            messages.error(request, "Будь ласка, заповніть всі поля форми.")
            return redirect('partner_form')

        info_models.PartnerRequest.objects.create(
            name=name,
            phone_code=phone_code,
            phone=phone,
            email=email,
            city=city,
            description=description,
        )

        messages.success(request, "Дякуємо! Ваш запит було успішно відправлено.")
        return redirect('about_us')

    return render(request, 'aboutus.html')


def feedback_form_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        country_code = request.POST.get('country_code')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')
        topic = request.POST.get('topic')

        # Сохранение данных в базу
        info_models.Feedback.objects.create(
            email=email,
            username=username,
            country_code=country_code,
            phone_number=phone_number,
            message=message,
            topic=topic
        )
        return redirect('index')

    return render(request, 'feedback_form.html')
