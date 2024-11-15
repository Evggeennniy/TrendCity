from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View
from catalog import models as catalog_models
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.db.models import Count, Q, Min, Max, Subquery, OuterRef
from collections import defaultdict
import json


class PanelView(View):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        categories = catalog_models.Category.objects.all()
        brands = catalog_models.ProductBrand.objects.all()

        promo_products = catalog_models.Product.objects.filter(
            included_in_promo=True
        ).prefetch_related('images').select_related('related_category', 'brand')

        top_products = catalog_models.Product.objects.filter(
            included_in_top=True
        ).prefetch_related('images').select_related('related_category', 'brand')

        recomend_products = catalog_models.Product.objects.filter(
            included_in_recomends=True
        ).prefetch_related('images').select_related('related_category', 'brand')

        filtered_top_products = defaultdict(list)
        for product in top_products:
            category = product.related_category
            filtered_top_products[category].append(product)

        context.update({
            'categories': categories,
            'brands': brands,
            'promo_products': promo_products,
            'top_products': top_products,
            'recomend_products': recomend_products,
            'filtered_top_products': filtered_top_products
        })
        return context


class IndexView(PanelView, TemplateView):
    template_name = "index.html"


class CatalogView(PanelView, ListView):
    model = catalog_models.Product
    template_name = "catalog.html"
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        queryset = catalog_models.Product.objects.all().prefetch_related('images', 'volumes')

        if category_id:
            queryset = queryset.filter(related_category_id=category_id)

        request = self.request

        search_query = request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(related_category__name__icontains=search_query)
            )

        brands = request.GET.getlist('brand')
        if brands:
            queryset = queryset.filter(brand__id__in=brands)

        stickers = []
        if request.GET.get('new_items'):
            stickers.append('new')
        if request.GET.get('top_items'):
            stickers.append('top')
        if stickers:
            queryset = queryset.filter(special_sticker__in=stickers)

        genders = request.GET.getlist('gender')
        if genders:
            queryset = queryset.filter(gender_for__in=genders)

        discount_items = request.GET.get('discount_items')
        all_items = request.GET.get('all_items')

        # Подзапрос для получения первого элемента volumes
        first_volume_discount = catalog_models.ProductVolume.objects.filter(
            # Замените your_model_name на вашу модель, которая связана через ManyToMany
            related=OuterRef('id')
        ).order_by('id').values('discount')[:1]  # Сортировка может быть изменена на ваше усмотрение

        # Применение аннотации
        queryset = queryset.annotate(first_volume_discount=Subquery(first_volume_discount))

        if discount_items:
            queryset = queryset.filter(first_volume_discount__gt=0)
        elif all_items and not discount_items:
            queryset = queryset.filter(first_volume_discount=0)
        elif discount_items and all_items:
            pass
        else:
            pass

        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price and max_price:
            try:
                min_price = int(min_price)
                max_price = int(max_price)
                queryset = queryset.filter(
                    volumes__price__gte=min_price,
                    volumes__price__lte=max_price
                )
            except ValueError:
                pass

        min_price_subquery = catalog_models.ProductVolume.objects.filter(
            related=OuterRef('pk')
        ).values('related').annotate(
            min_price=Min('price')
        ).values('min_price')

        queryset = queryset.annotate(
            min_price=Subquery(min_price_subquery)
        )

        sort_option = request.GET.get('sort')
        if sort_option == 'price_asc':
            queryset = queryset.order_by('min_price')
        elif sort_option == 'price_desc':
            queryset = queryset.order_by('-min_price')
        elif sort_option == 'name_asc':
            queryset = queryset.order_by('name')
        elif sort_option == 'name_desc':
            queryset = queryset.order_by('-name')
        else:
            queryset = queryset.order_by('id')

        queryset = queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = catalog_models.ProductBrand.objects.all()
        context['selected_brands'] = list(map(int, self.request.GET.getlist('brand')))
        context['selected_genders'] = self.request.GET.getlist('gender')
        context['selected_new_items'] = self.request.GET.get('new_items')
        context['selected_top_items'] = self.request.GET.get('top_items')
        context['selected_discount_items'] = self.request.GET.get('discount_items')
        context['selected_all_items'] = self.request.GET.get('all_items')
        context['min_price'] = self.request.GET.get('min_price', '0')
        context['max_price'] = self.request.GET.get('max_price', '2000')
        context['search_query'] = self.request.GET.get('q', '')

        sort_option = self.request.GET.get('sort')
        if sort_option == 'price_asc':
            context['current_sort_label'] = 'Ціна: за зростанням'
        elif sort_option == 'price_desc':
            context['current_sort_label'] = 'Ціна: за спаданням'
        elif sort_option == 'name_asc':
            context['current_sort_label'] = 'Назва: від А до Я'
        elif sort_option == 'name_desc':
            context['current_sort_label'] = 'Назва: від Я до А'
        else:
            context['current_sort_label'] = None

        context['current_sort'] = sort_option

        return context


class ProductDetailsView(PanelView, DetailView):
    queryset = catalog_models.Product.objects.annotate(
        active_reviews_count=Count('reviews', filter=Q(reviews__active=True))
    ).prefetch_related(
        'images', 'volumes', 'options', 'wrappers',
        'accesories', 'accesories__images', 'reviews', 'related_category__promos'
    ).select_related('brand', 'related_category')

    template_name = 'product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        context['active_reviews_count'] = product.active_reviews_count
        return context


def add_review(request, pk):
    product = get_object_or_404(catalog_models.Product, id=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        text = request.POST.get('text', '').strip()
        rating = request.POST.get('rating', '').strip()

        if not all([name, text, rating]):
            # Вы можете добавить сообщение об ошибке или перенаправить обратно с сообщением
            return redirect(reverse('product', args=[product.pk]))

        catalog_models.ProductReview.objects.create(
            product=product,
            name=name,
            text=text,
            rating=rating,
        )

        return redirect(reverse('product', args=[product.pk]))
    else:
        return redirect(reverse('product', args=[product.pk]))


def order_submit(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        name = data.get('name')
        surname = data.get('surname')
        country_code = data.get('country_code')
        number = data.get('number')
        payment_method = data.get('payment_method')
        post_office_id = data.get('post_office_id')
        comment = data.get('comment')
        post_office = data.get('delivery_type')

        order_content = data.get('order_list')

        order = catalog_models.Order.objects.create(
            name=name,
            surname=surname,
            country_code=country_code,
            number=number,
            payment_method=payment_method,
            post_office=post_office,
            post_office_id=post_office_id,
            comment=comment,
        )

        order_content = [
            catalog_models.OrderPart.objects.create(
                related_order=order,
                product=catalog_models.Product.objects.filter(id=item.get('productId')).first(),
                count=item.get('productQuantity'),
                volume=catalog_models.ProductVolume.objects.filter(id=item.get('volumeId')).first(),
                wrapper=catalog_models.ProductWrapper.objects.filter(id=item.get('wrapperId')).first()
            ) for item in order_content
        ]

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
