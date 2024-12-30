from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext as _


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
        ("men", _("чоловіче")),
        ("women", _("жіноче")),
        ("unisex", _("унісекс")),
    ]

    STICKER_CHOICES = [("top", "топ товар"), ("new", "новинка"), ("promo", "акцiя")]

    name = models.CharField(verbose_name="Назва", max_length=64)
    short_desc = CKEditor5Field(
        verbose_name="Короткий опис", config_name="default", max_length=256
    )
    description = CKEditor5Field(
        verbose_name="Опис", config_name="default", max_length=2048
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
        return f"{self.value}/{self.get_curr_price()} ₴"


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

    def get_telegram_text_free(self):
        return f"{self.name}:0₴"

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
    promo_category = models.ForeignKey(
        Category,
        verbose_name="Безкоштовна категорія",
        blank=True,
        related_name="free_promo_category",
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
    promocode = models.CharField(verbose_name="Промокод", max_length=16)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    def get_telegram_text(self):
        order_parts = self.order_items.all()
        parts_text = "\n".join([part.get_telegram_text() for part in order_parts])

        order_parts_present = self.order_items_present.all()
        parts_text_present = "\n".join(
            [part.get_telegram_text() for part in order_parts_present]
        )

        promocode_text = f"Промокод: {self.promocode}\n " if self.promocode else ""
        comment_text = f"Коментар: {self.comment}\n" if self.comment else ""
        present_text = (
            f"🎁 Подарунки:\n\n{parts_text_present}\n\n" if parts_text_present else ""
        )
        promotion_text = (
            f"🛍 Застосовані акції та промокоди:\n{self.promotion_text }\n\n"
            if self.promotion_text
            else ""
        )
        return (
            f"Дата та час замовлення: {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"🛒 Замовлення від {self.name} {self.surname}:\n"
            f"Номер телефону: +{self.country_code}{self.number.replace(' ','')}\n"
            f"Спосіб оплати: {self.payment_method}\n"
            f"Пошта: {self.post_office}/{self.post_office_id}\n"
            f"{promocode_text}{comment_text}\n"
            f"{promotion_text}{present_text}"
            "📦 Товари:\n\n"
            f"{parts_text}"
            f"Всього: {self.full_price} ₴\n"
        )


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

        volume = f"Об'єм: {self.volume.get_telegram_text()};\n" if self.volume else ""
        wrapper = (
            f"Обертка: {self.wrapper.get_telegram_text()};\n" if self.wrapper else ""
        )

        return f"{self.product.get_telegram_text()}/{self.count}шт.\n{volume}{wrapper}"


class OrderPartPresent(models.Model):
    related_order = models.ForeignKey(
        verbose_name="Відношення до замовлення",
        to=Order,
        on_delete=models.CASCADE,
        related_name="order_items_present",
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
        verbose_name = "Подарунки🎁"
        verbose_name_plural = "Подарунки🎁"

    def get_telegram_text(self):
        """
        Формує красивий текст для однієї частини замовлення.
        """

        volume = f"Об'єм: {self.volume.get_telegram_text()};\n" if self.volume else ""
        wrapper = (
            f"Обертка: {self.wrapper.get_telegram_text_free()};\n"
            if self.wrapper
            else ""
        )

        return f"{self.product.get_telegram_text()}/{self.count}шт.\n{volume}{wrapper}"


class Payment(models.Model):
    """
    Модель бази даних платежів.
    """

    order = models.ForeignKey(
        verbose_name="Кліент", to=Order, on_delete=models.SET_NULL, null=True
    )
    summary_price = models.DecimalField(
        verbose_name="Сума", max_digits=10, decimal_places=2
    )
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True, blank=True)

    def __str__(self) -> str:
        return f"Платіж {self.id}, сума {self.summary_price}, дата {self.date}"

    class Meta:
        verbose_name = "Платіж"
        verbose_name_plural = "Платежі"

    def get_telegram_text(self):
        return (
            f"✅Успішно оплачено {self.date.strftime('%Y-%m-%d %H:%M:%S')}, сума {self.summary_price}₴\n"
            f"Дата та час замовлення: {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"🛒 Замовлення від {self.name} {self.surname}:\n"
        )
