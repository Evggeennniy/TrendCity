from django.contrib import admin
from django.urls import include, path
from catalog import views as catalog_views

urlpatterns = [
    path("", catalog_views.IndexView.as_view(), name="index"),
    path("catalog/", catalog_views.CatalogView.as_view(), name="catalog"),
    path("basket/", catalog_views.get_basket, name="basket"),
    path("catalog/<int:pk>/", catalog_views.CatalogView.as_view(), name="catalog"),
    path("product/<int:pk>/", catalog_views.ProductDetailsView.as_view(), name="product"),
    path("product/<int:pk>/add_review/", catalog_views.add_review, name="add_review"),
    path("submit-order/", catalog_views.order_submit, name="order_submit"),
    path('liqpay', catalog_views.LiqPayView.as_view(), name='liqpay'),
    path('liqpay_callback', catalog_views.LiqPayCallbackView.as_view(), name='liqpay_callback'),
]
