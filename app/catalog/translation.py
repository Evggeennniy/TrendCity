from modeltranslation.translator import register, TranslationOptions
from .models import (
    Category,
    ProductBrand,
    Product,
    ProductVolume,
    ProductOption,
    ProductWrapper,
    Promotion,
    Promocode,
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
    fields = ("name",)


@register(Promocode)
class PromocodeTranslationOptions(TranslationOptions):
    fields = ("name",)
