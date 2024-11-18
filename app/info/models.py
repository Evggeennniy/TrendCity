from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class PartnerRequest(models.Model):
    name = models.CharField(max_length=255, verbose_name="Ім'я")
    phone_code = models.CharField(max_length=10, verbose_name="Код країни")
    phone = models.CharField(max_length=20, verbose_name="Номер телефону")
    email = models.EmailField(verbose_name="Ел. пошта")
    city = models.CharField(max_length=100, verbose_name="Місто")
    description = models.TextField(verbose_name="Опис бізнесу")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачі")

    def __str__(self):
        return f"Запит від {self.name} ({self.email})"

    class Meta:
        verbose_name = "Запит партнера"
        verbose_name_plural = "Запити партнерів"


class Feedback(models.Model):
    email = models.EmailField(verbose_name='Ел. пошта', max_length=254)
    username = models.CharField(verbose_name='Ім’я', max_length=100)
    country_code = models.CharField(verbose_name='Код країни', max_length=5)
    phone_number = models.CharField(verbose_name='Номер телефону', max_length=20)
    message = models.TextField(verbose_name='Ваш лист')
    topic = models.CharField(verbose_name='Тема', max_length=50)

    def __str__(self):
        return f"{self.username} - {self.email}"

    class Meta:
        verbose_name = "Запит на зв'язок"
        verbose_name_plural = "Запити на зв'язок"


class AboutUsHeader(models.Model):
    text = CKEditor5Field(verbose_name='Текст', config_name='default', max_length=500)

    class Meta:
        verbose_name = "Iнфо блок (О нас/Заголовок)"
        verbose_name_plural = "Iнфо блоки (О нас/Заголовок)"


class AboutUsForClients(models.Model):
    icon = models.FileField(verbose_name='Значок', upload_to='icons')
    header = models.CharField(verbose_name='Заголовок', max_length=26)
    text = CKEditor5Field(verbose_name='Текст', config_name='default', max_length=500)

    class Meta:
        verbose_name = "Iнфо блок (О нас/Для покупців)"
        verbose_name_plural = "Iнфо блоки (О нас/Для покупців)"


class AboutUsForm(models.Model):
    text = CKEditor5Field(verbose_name='Текст', config_name='default', max_length=500)

    class Meta:
        verbose_name = "Iнфо блок (О нас/Форма)"
        verbose_name_plural = "Iнфо блоки (О нас/Форма)"


class AboutUsReview(models.Model):
    grade = models.CharField(verbose_name='Оцiнка', max_length=12)
    text = CKEditor5Field(verbose_name='Текст', config_name='default', max_length=200)
    name = models.CharField(verbose_name="Iм'я та Призвище", max_length=48)

    class Meta:
        verbose_name = "Iнфо блок (О нас/Вiдгук)"
        verbose_name_plural = "Iнфо блоки (О нас/Вiдгук)"


class ContactText(models.Model):
    icon = models.FileField(verbose_name='Значок', upload_to='icons')
    header = models.CharField(verbose_name='Заголовок', max_length=16)
    value = models.CharField(verbose_name='Значення', max_length=32)

    class Meta:
        verbose_name = "Iнфо блок (Контакти/Текстове)"
        verbose_name_plural = "Iнфо блоки (Контакти/Текстове)"


class ContactLink(models.Model):
    icon = models.FileField(verbose_name='Значок', upload_to='icons')
    header = models.CharField(verbose_name='Заголовок', max_length=16)
    link = models.CharField(verbose_name='Посилання', max_length=128)

    class Meta:
        verbose_name = "Iнфо блок (Контакти/Посылання)"
        verbose_name_plural = "Iнфо блоки (Контакти/Посылання)"


class PrivacyPolicy(models.Model):
    text = CKEditor5Field(verbose_name='Текст', config_name='default', max_length=2000)

    class Meta:
        verbose_name = "Iнфо блок (Політика конфеденційності)"
        verbose_name_plural = "Iнфо блоки (Політика конфеденційності)"


class PublicOfferАgreement(models.Model):
    text = CKEditor5Field(verbose_name='Текст', config_name='default', max_length=2000)

    class Meta:
        verbose_name = "Iнфо блок (Договір публічної оферти)"
        verbose_name_plural = "Iнфо блоки (Договір публічної оферти)"
