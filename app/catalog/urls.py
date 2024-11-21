from django.contrib import admin
from django.urls import include, path
from catalog import views as catalog_views

urlpatterns = [
    path('', catalog_views.IndexView.as_view(), name='index'),
    path('catalog/', catalog_views.CatalogView.as_view(), name='catalog'),
    path('catalog/<int:pk>/', catalog_views.CatalogView.as_view(), name='catalog'),
    path('product/<int:pk>/', catalog_views.ProductDetailsView.as_view(), name='product'),
    path('product/<int:pk>/add_review/', catalog_views.add_review, name='add_review'),
    path('submit-order/', catalog_views.order_submit, name='order_submit'),
    path('check-promocode/<str:promocode>/', catalog_views.check_promocode, name='check_promo'),
]
