from django.contrib import admin
from catalog import models as catalog_models


@admin.register(catalog_models.Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("name",)

    search_fields = ("id", "name")

    readonly_fields = ()


@admin.register(catalog_models.ProductBrand)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ("name",)

    search_fields = ("id", "name")

    readonly_fields = ()


class ProductImageInline(admin.TabularInline):
    model = catalog_models.ProductImage
    extra = 1


class ProductOptionInline(admin.TabularInline):
    model = catalog_models.ProductOption
    extra = 1


class ProductVolumeInline(admin.TabularInline):
    model = catalog_models.ProductVolume
    extra = 1


class ProductWrapperInline(admin.TabularInline):
    model = catalog_models.ProductWrapper
    extra = 1


@admin.register(catalog_models.Product)
class ProductsAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
        ProductOptionInline,
        ProductVolumeInline,
        ProductWrapperInline,
    ]

    list_display = ("name", "special_sticker")

    search_fields = ("id", "name")

    readonly_fields = ()


@admin.register(catalog_models.ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "name", "rating", "created_at")
    list_filter = ("product", "rating", "created_at")
    search_fields = ("name", "text", "product__name")
    readonly_fields = ("product", "name", "text", "rating", "created_at")

    def has_add_permission(self, request):
        return False


@admin.register(catalog_models.FreeProductPromotion)
class FreeProductPromotionAdmin(admin.ModelAdmin):
    list_display = ("name", "promo_product", "promo_count")
    search_fields = ("promo_product__name",)
    list_filter = ("applicable_categories",)


@admin.register(catalog_models.QuantityDiscountPromotion)
class QuantityDiscountPromotionAdmin(admin.ModelAdmin):
    list_display = ("name", "promo_quantity", "promo_discount")
    search_fields = ("promo_discount",)
    list_filter = ("applicable_categories",)


@admin.register(catalog_models.PriceDiscountPromotion)
class PriceDiscountPromotionAdmin(admin.ModelAdmin):
    list_display = ("name", "promo_price", "promo_discount")
    search_fields = ("promo_price",)
    list_filter = ("applicable_categories",)


@admin.register(catalog_models.FreeDeliveryPromotion)
class FreeDeliveryPromotionAdmin(admin.ModelAdmin):
    list_display = ("name", "promo_controller", "promo_value")
    search_fields = ("promo_controller",)
    list_filter = ("applicable_categories", "promo_controller")


# Promocode Model Configuration
@admin.register(catalog_models.Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ("name", "discount")
    search_fields = ("name",)


# Order and OrderPart Models Configuration
class OrderPartInline(admin.TabularInline):
    model = catalog_models.OrderPart
    extra = 1


@admin.register(catalog_models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("datetime", "name", "surname")
    inlines = [OrderPartInline]


@admin.register(catalog_models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass