from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
import json


class Category(models.Model):
    icon = models.FileField(verbose_name="Значок", upload_to="icons")
    image = models.FileField(verbose_name="Зображення", upload_to="images")
    name = models.CharField(verbose_name="Назва", max_length=16)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class ProductBrand(models.Model):
    logotype = models.FileField(verbose_name="Лого", upload_to="logos")
    name = models.CharField(verbose_name="Назва", max_length=16)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренди"


class Product(models.Model):
    GENDER_CHOICES = [
        ("men", "чоловіче"),
        ("women", "жіноче"),
        ("unisex", "унісекс"),
    ]

    STICKER_CHOICES = [("top", "топ товар"), ("new", "новинка"), ("promo", "акцiя")]

    name = models.CharField(verbose_name="Назва", max_length=64)
    description = CKEditor5Field(
        verbose_name="Опис", config_name="default", max_length=256
    )
    brand = models.ForeignKey(
        verbose_name="Бренд",
        to=ProductBrand,
        on_delete=models.CASCADE,
        related_name="products",
    )
    gender_for = models.CharField(
        verbose_name="Cтать", max_length=6, choices=GENDER_CHOICES
    )
    special_sticker = models.CharField(
        verbose_name="Стiкер", max_length=6, choices=STICKER_CHOICES, blank=True
    )
    related_accesories = models.ManyToManyField(
        verbose_name="Аксесуари",
        to="self",
        related_name="accesories",
        symmetrical=False,
        blank=True,
    )
    related_category = models.ForeignKey(
        verbose_name="Категорiя",
        to=Category,
        on_delete=models.CASCADE,
        related_name="products",
    )
    included_in_promo = models.BooleanField(
        verbose_name="Включений у акцiйний блок", default=False
    )
    included_in_top = models.BooleanField(
        verbose_name="Включений у топ блок", default=False
    )
    included_in_recomends = models.BooleanField(
        verbose_name="Включений у рекоменд. блок", default=False
    )

    def __str__(self) -> str:
        return self.name

    def get_avg_review(self):
        reviews = self.reviews.filter(active=True)
        if not reviews:
            return 0
        reviews = sum([item.rating for item in reviews]) / len(reviews)
        return round(reviews, 1)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def get_telegram_text(self):
        return self.name


class ProductImage(models.Model):
    image = models.FileField(verbose_name="Зображення", upload_to="product_images")
    related = models.ForeignKey(
        verbose_name="Відноситься до",
        to=Product,
        on_delete=models.CASCADE,
        related_name="images",
    )

    def __str__(self) -> str:
        return "Зображення товару"

    class Meta:
        verbose_name = "Зображення товару"
        verbose_name_plural = "Зображення товарiв"


class ProductVolume(models.Model):
    value = models.CharField(verbose_name="Опцiя", max_length=8)
    price = models.IntegerField(verbose_name="Цiна")
    discount = models.IntegerField(verbose_name="Знижка %", default=0)
    related = models.ForeignKey(
        verbose_name="Відноситься до",
        to=Product,
        on_delete=models.CASCADE,
        related_name="volumes",
    )

    def __str__(self) -> str:
        return f"Опцiя об'єму {self.value}"

    def get_curr_price(self):
        if self.discount:
            return self.price - (self.price / 100 * self.discount)
        return round(self.price, 1)

    class Meta:
        verbose_name = "Опцiя об'єму"
        verbose_name_plural = "Опцiї об'єму"

    def get_telegram_text(self):
        return f"{self.value}/{self.price}/{self.discount}%"


class ProductOption(models.Model):
    name = models.CharField(verbose_name="Назва", max_length=32)
    related = models.ForeignKey(
        verbose_name="Відноситься до",
        to=Product,
        on_delete=models.CASCADE,
        related_name="options",
    )

    def __str__(self) -> str:
        return "Варіант різновиду"

    class Meta:
        verbose_name = "Опцiя різновиду"
        verbose_name_plural = "Опцiї різновидiв"


class ProductWrapper(models.Model):
    name = models.CharField(verbose_name="Назва", max_length=32)
    image = models.FileField(verbose_name="Зображення", upload_to="wrapper_images")
    price = models.IntegerField(verbose_name="Ціна")
    related = models.ForeignKey(
        verbose_name="Відноситься до",
        to=Product,
        on_delete=models.CASCADE,
        related_name="wrappers",
    )

    def __str__(self) -> str:
        return self.name

    def get_telegram_text(self):
        return f"{self.name}:{self.price}"

    class Meta:
        verbose_name = "Обгортка продукту"
        verbose_name_plural = "Обгортки продуктiв"


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews", verbose_name="Товар"
    )
    name = models.CharField(max_length=100, verbose_name="Ім'я")
    text = models.TextField(verbose_name="Текст відгуку")
    rating = models.DecimalField(
        max_digits=2, decimal_places=1, verbose_name="Оцінка", default=0
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    active = models.BooleanField(verbose_name="Активний", default=False)

    def __str__(self):
        return f"Відгук від {self.name} для {self.product.name}"

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"


class Promotion(models.Model):
    name = models.CharField(max_length=50, verbose_name="Заголовок акції")
    applicable_categories = models.ManyToManyField(
        Category, verbose_name="Застосовні категорії", blank=True, related_name="promos"
    )

    def __str__(self):
        return self.name


class FreeProductPromotion(Promotion):
    promo_count = models.IntegerField(verbose_name="Кількість товару")
    promo_product = models.ForeignKey(
        Product,
        verbose_name="Бесплатный товар",
        blank=True,
        related_name="free_promo_product",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Акцiя"
        verbose_name_plural = "Акції (Безкоштовний товар)"


class QuantityDiscountPromotion(Promotion):
    promo_quantity = models.IntegerField(
        verbose_name="Кількість товару однієї категорії"
    )
    promo_discount = models.IntegerField(verbose_name="Вiдсоток знижки")

    class Meta:
        verbose_name = "Акцiя"
        verbose_name_plural = "Акції (Знижка на кількість)"


class PriceDiscountPromotion(Promotion):
    promo_price = models.IntegerField(verbose_name="Сумма замовлення")
    promo_discount = models.IntegerField(verbose_name="Вiдсоток знижки")

    class Meta:
        verbose_name = "Акцiя"
        verbose_name_plural = "Акції (Знижка на суму замовлення)"


class FreeDeliveryPromotion(Promotion):
    CONTROLLERS_CHOICES = [
        ("count", "Кiлькiсть"),
        ("price", "Цiна"),
    ]
    promo_controller = models.CharField(
        verbose_name="Орієнтація на", max_length=12, choices=CONTROLLERS_CHOICES
    )
    promo_value = models.IntegerField(verbose_name="Значення")

    class Meta:
        verbose_name = "Акцiя"
        verbose_name_plural = "Акції (Безкоштовна доставка)"


class Promocode(models.Model):
    name = models.CharField(verbose_name="Промокод", max_length=50)
    discount = models.IntegerField(verbose_name="Знижка")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоди"


class Order(models.Model):
    datetime = models.DateTimeField(
        verbose_name="Дата та час замовлення", auto_now_add=True
    )
    name = models.CharField(verbose_name="Iм'я", max_length=20)
    surname = models.CharField(verbose_name="Прізвище", max_length=20)
    country_code = models.CharField(verbose_name="Код країни", max_length=3)
    number = models.CharField(verbose_name="Номер", max_length=12)
    payment_method = models.CharField(verbose_name="Тип оплати", max_length=50)
    post_office = models.CharField(verbose_name="Пошта", max_length=20)
    post_office_id = models.CharField(verbose_name="Вiддiлення", max_length=20)
    full_price = models.DecimalField(
        verbose_name="Цiна", max_digits=12, decimal_places=2
    )
    comment = models.CharField(verbose_name="Коментар", max_length=256)
    promotion_text = models.CharField(
        verbose_name="🎁🛒 Застосовані акції та промокоди:",
        max_length=1024,
        default="No promotion",
    )
    present_text = models.CharField(
        verbose_name="🎁 Подарунки",
        max_length=1024,
        default="No promotion",
    )
    promocode = models.CharField(verbose_name="Промокод", max_length=16)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    def get_telegram_text(self):
        country_names = {
            "380": "🇺🇦 Україна",
        }

        country_name = country_names.get(self.country_code, "Невідомо")
        order_parts = self.order_items.all()
        parts_text = "\n".join([part.get_telegram_text() for part in order_parts])
        return f"""\
        🛒 Замовлення від {self.name} {self.surname}:
        Країна: {country_name} (Код: {self.country_code})
        Номер телефону: {self.number}
        Спосіб оплати: {self.payment_method}
        Пошта: {self.post_office}
        Відділення: {self.post_office_id}
        Ціна: {self.full_price} грн
        Промокод: {self.promocode}
        Коментар: {self.comment}
        Дата та час замовлення: {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}
        🎁 Застосовані акції та промокоди:
        {self.promotion_text}
        🎁 Подарунки:
        {self.present_text}
        📦 Товари:
        {parts_text}       
        """


class OrderPart(models.Model):
    related_order = models.ForeignKey(
        verbose_name="Відношення до замовлення",
        to=Order,
        on_delete=models.CASCADE,
        related_name="order_items",
    )
    product = models.ForeignKey(
        verbose_name="Товар", to=Product, on_delete=models.SET_NULL, null=True
    )
    count = models.IntegerField(verbose_name="Кiлькiсть")
    volume = models.ForeignKey(
        verbose_name="Об'ем", to=ProductVolume, on_delete=models.SET_NULL, null=True
    )
    wrapper = models.ForeignKey(
        verbose_name="Обертка", to=ProductWrapper, on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name = "Подробицi замовлення"
        verbose_name_plural = "Подробицi замовлень"

    def get_telegram_text(self):
        """
        Формує красивий текст для однієї частини замовлення.
        """
        product_name = self.product.get_telegram_text() if self.product else "Невідомо"
        volume = self.volume.get_telegram_text() if self.volume else "Невідомо"
        wrapper = self.wrapper.get_telegram_text() if self.wrapper else "Невідомо"

        return f"- Товар: {product_name}, Кількість: {self.count}, Об'єм: {volume}, Обертка: {wrapper}"
