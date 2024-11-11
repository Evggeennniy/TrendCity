from django.db import models


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
        verbose_name_plural = "Запити на зв'язки"
