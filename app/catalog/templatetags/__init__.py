# app_name/templatetags/custom_filters.py
from django import template
from django.utils.translation import get_language

register = template.Library()


@register.simple_tag
def generate_new_url(request):
    current_lang = get_language()  # Отримуємо поточну мову
    full_path = request.get_full_path()

    if current_lang == "ru":
        new_url = full_path.replace("/ru", "")
    else:
        new_url = "/ru" + full_path

    return new_url
