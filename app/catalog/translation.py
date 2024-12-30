from modeltranslation.translator import register, TranslationOptions
from .models import (
    Category,
    ProductBrand,
    Product,
    ProductVolume,
    ProductOption,
    ProductWrapper,
    Promotion,
    Promocode, FreeDeliveryPromotion, PriceDiscountPromotion, QuantityDiscountPromotion, FreeProductPromotion,
)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(ProductBrand)
class ProductBrandTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ("name", "short_desc", "description", "special_sticker")


@register(ProductVolume)
class ProductVolumeTranslationOptions(TranslationOptions):
    fields = ("value",)


@register(ProductOption)
class ProductOptionTranslationOptions(TranslationOptions):
    fields = ("name",)

@register(ProductWrapper)
class ProductWrapperTranslationOptions(TranslationOptions):
    fields = ("name",)

@register(Promotion)
class PromotionTranslationOptions(TranslationOptions):
    pass

@register(FreeDeliveryPromotion)
class FreeDeliveryPromotionTranslationOptions(TranslationOptions):
    fields = ("name",)

@register(PriceDiscountPromotion)
class FreeDeliveryPromotionTranslationOptions(TranslationOptions):
    fields = ("name",)

@register(QuantityDiscountPromotion)
class QuantityDiscountPromotionTranslationOptions(TranslationOptions):
    fields = ("name",)

@register(FreeProductPromotion)
class FreeProductPromotionTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Promocode)
class PromocodeTranslationOptions(TranslationOptions):
    fields = ("name",)
