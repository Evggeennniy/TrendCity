import os

from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import TemplateView, ListView, DetailView, View
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.db.models import Count, Q, Min, Max, Subquery, OuterRef
from collections import defaultdict
import json

from liqpay.liqpay3 import LiqPay
from .utils import send_telegram_message
from catalog import basket, models as catalog_models
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Payment


class PanelView(View):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        categories = catalog_models.Category.objects.all()
        brands = catalog_models.ProductBrand.objects.all()

        promo_products = (
            catalog_models.Product.objects.filter(included_in_promo=True)
            .prefetch_related("images")
            .select_related("related_category", "brand")
        )

        top_products = (
            catalog_models.Product.objects.filter(included_in_top=True)
            .prefetch_related("images")
            .select_related("related_category", "brand")
        )

        recomend_products = (
            catalog_models.Product.objects.filter(included_in_recomends=True)
            .prefetch_related("images")
            .select_related("related_category", "brand")
        )

        filtered_top_products = defaultdict(list)
        for product in top_products:
            category = product.related_category
            filtered_top_products[category].append(product)

        context.update(
            {
                "categories": categories,
                "brands": brands,
                "promo_products": promo_products,
                "top_products": top_products,
                "recomend_products": recomend_products,
                "filtered_top_products": filtered_top_products,
            }
        )
        return context


class IndexView(PanelView, TemplateView):
    template_name = "index.html"


class CatalogView(PanelView, ListView):
    model = catalog_models.Product
    template_name = "catalog.html"
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs.get("pk")
        queryset = catalog_models.Product.objects.all().prefetch_related(
            "images", "volumes"
        )

        if category_id:
            queryset = queryset.filter(related_category_id=category_id)

        request = self.request

        search_query = request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(related_category__name__icontains=search_query)
            )

        brands = request.GET.getlist("brand")
        if brands:
            queryset = queryset.filter(brand__id__in=brands)

        stickers = []
        if request.GET.get("new_items"):
            stickers.append("new")
        if request.GET.get("top_items"):
            stickers.append("top")
        if stickers:
            queryset = queryset.filter(special_sticker__in=stickers)

        genders = request.GET.getlist("gender")
        if genders:
            queryset = queryset.filter(gender_for__in=genders)

        discount_items = request.GET.get("discount_items")
        all_items = request.GET.get("all_items")

        # Подзапрос для получения первого элемента volumes
        first_volume_discount = (
            catalog_models.ProductVolume.objects.filter(
                # З��ените your_model_name на вашу модель, которая связана через ManyToMany
                related=OuterRef("id")
            )
            .order_by("id")
            .values("discount")[:1]
        )  # Сортировка может быть изменена на ваше усмотрение

        # Применение аннотации
        queryset = queryset.annotate(
            first_volume_discount=Subquery(first_volume_discount)
        )

        if discount_items:
            queryset = queryset.filter(first_volume_discount__gt=0)
        elif all_items and not discount_items:
            queryset = queryset.filter(first_volume_discount=0)
        elif discount_items and all_items:
            pass
        else:
            pass

        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        if min_price and max_price:
            try:
                min_price = int(min_price)
                max_price = int(max_price)
                queryset = queryset.filter(
                    volumes__price__gte=min_price, volumes__price__lte=max_price
                )
            except ValueError:
                pass

        min_price_subquery = (
            catalog_models.ProductVolume.objects.filter(related=OuterRef("pk"))
            .values("related")
            .annotate(min_price=Min("price"))
            .values("min_price")
        )

        queryset = queryset.annotate(min_price=Subquery(min_price_subquery))

        sort_option = request.GET.get("sort")
        if sort_option == "price_asc":
            queryset = queryset.order_by("min_price")
        elif sort_option == "price_desc":
            queryset = queryset.order_by("-min_price")
        elif sort_option == "name_asc":
            queryset = queryset.order_by("name")
        elif sort_option == "name_desc":
            queryset = queryset.order_by("-name")
        else:
            queryset = queryset.order_by("id")

        queryset = queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brands"] = catalog_models.ProductBrand.objects.all()
        context["selected_brands"] = list(map(int, self.request.GET.getlist("brand")))
        context["selected_genders"] = self.request.GET.getlist("gender")
        context["selected_new_items"] = self.request.GET.get("new_items")
        context["selected_top_items"] = self.request.GET.get("top_items")
        context["selected_discount_items"] = self.request.GET.get("discount_items")
        context["selected_all_items"] = self.request.GET.get("all_items")
        context["min_price"] = self.request.GET.get("min_price", "0")
        context["max_price"] = self.request.GET.get("max_price", "2000")
        context["search_query"] = self.request.GET.get("q", "")

        sort_option = self.request.GET.get("sort")
        if sort_option == "price_asc":
            context["current_sort_label"] = "Ціна: за зростанням"
        elif sort_option == "price_desc":
            context["current_sort_label"] = "Ціна: за спаданням"
        elif sort_option == "name_asc":
            context["current_sort_label"] = "Назва: від А до Я"
        elif sort_option == "name_desc":
            context["current_sort_label"] = "Назва: від Я до А"
        else:
            context["current_sort_label"] = None

        context["current_sort"] = sort_option

        return context


class ProductDetailsView(PanelView, DetailView):
    queryset = (
        catalog_models.Product.objects.annotate(
            active_reviews_count=Count("reviews", filter=Q(reviews__active=True))
        )
        .prefetch_related(
            "images",
            "volumes",
            "options",
            "wrappers",
            "accesories",
            "accesories__images",
            "reviews",
            "related_category__promos",
        )
        .select_related("brand", "related_category")
    )

    template_name = "product.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        context["active_reviews_count"] = product.active_reviews_count
        return context


def add_review(request, pk):
    product = get_object_or_404(catalog_models.Product, id=pk)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        text = request.POST.get("text", "").strip()
        rating = request.POST.get("rating", "").strip()

        if not all([name, text, rating]):
            # Вы можете добавить сообщение об ошибке или перенаправить обратно с сообщением
            return redirect(reverse("product", args=[product.pk]))

        catalog_models.ProductReview.objects.create(
            product=product,
            name=name,
            text=text,
            rating=rating,
        )

        return redirect(reverse("product", args=[product.pk]))
    else:
        return redirect(reverse("product", args=[product.pk]))


def order_submit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        surname = data.get("surname")
        country_code = data.get("countryCode")[1:]
        number = data.get("number")
        payment_method = data.get("paymentMethod")
        post_office_id = data.get("postOfficeId")
        comment = data.get("comment")
        post_office = data.get("postOffice")
        promocode_name = data.get("promocodeName", "")
        promocode_percent = data.get("promocodePercent", "")
        result = basket.calculate_basket(
            data.get("order_list"), data.get("promocodeName")
        )
        order_content = data.get("order_list")
        promotion_text = ";\n".join(result["discountLabel"])
        present_text = ";\n".join(result["present"])
        full_price = result["sumPrice"]
        promocode = (
            f"{promocode_name} / {promocode_percent}₴ / {result['promoCodeCof']} %"
            if promocode_name
            else ""
        )
        order = catalog_models.Order.objects.create(
            name=name,
            surname=surname,
            country_code=country_code,
            number=number,
            payment_method=payment_method,
            post_office=post_office,
            post_office_id=post_office_id,
            comment=comment,
            full_price=full_price,
            promotion_text=promotion_text,
            present_text=present_text,
            promocode=promocode,
        )

        order_content = [
            catalog_models.OrderPart.objects.create(
                related_order=order,
                product=catalog_models.Product.objects.filter(
                    id=item.get("productId")
                ).first(),
                count=item.get("productQuantity"),
                volume=catalog_models.ProductVolume.objects.filter(
                    id=item.get("volumeId")
                ).first(),
                wrapper=catalog_models.ProductWrapper.objects.filter(
                    id=item.get("wrapperId")
                ).first(),
            )
            for item in order_content
        ]
        is_liqpay = payment_method == "Оплата онлайн картою"

        send_telegram_message(order.get_telegram_text())
        return JsonResponse(
            {"status": "success", "is_liqpay": is_liqpay, "data": {"orderId": order.id}}
        )
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


def get_basket(request):
    try:
        if request.method == "POST":
            body = json.loads(request.body)
            data = basket.calculate_basket(
                body.get("order_list"), body.get("promocodeName")
            )

            return JsonResponse({"status": "success", "data": data})
        else:
            return JsonResponse({"error": "Invalid request"}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "Invalid request"}, status=400)


class LiqPayView(TemplateView):
    template_name = "liqpay_payment.html"

    def get(self, request, *args, **kwargs):
        # Спробуйте отримати замовлення з бази даних
        try:
            order = catalog_models.Order.objects.get(id=kwargs.get("order_id"))
        except catalog_models.Order.DoesNotExist:
            # Якщо замовлення не знайдено, перенаправте на кошик
            return redirect("/user/basket")

        # Перевіряємо, чи оплата вже була здійснена
        if Payment.objects.filter(order_id=order.id).exists():
            return redirect("/user/basket")

        # Перевіряємо, чи метод оплати не є "Оплата онлайн картою"
        if order.payment_method != "Оплата онлайн картою":
            return redirect("/user/basket")
        server_url = os.getenv("SERVER_URL")
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        params = {
            "action": "pay",
            "amount": str(order.full_price),
            "currency": "UAH",
            "description": f"Оплата на TrendCity, замовлення {order.id}",
            "order_id": str(order.id),
            "version": "3",
            "server_url": f"{server_url}/liqpay_callback",  # url to callback view
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        return render(
            request, self.template_name, {"signature": signature, "data": data}
        )


@method_decorator(csrf_exempt, name="dispatch")
class LiqPayCallbackView(View):
    def post(self, request):
        data = request.POST.get("data")
        signature = request.POST.get("signature")
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        sign = liqpay.str_to_sign(
            settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY
        )
        if sign == signature:
            response = liqpay.decode_data_from_str(data)
            order_id = response.get("order_id")
            summary_price = response.get("amount")
            pay =  Payment.objects.create(order_id=order_id, summary_price=summary_price)
            send_telegram_message(pay.get_telegram_text())
            return JsonResponse({"status": "success", "data": response})
        return JsonResponse({"error": "Invalid request"}, status=400)
