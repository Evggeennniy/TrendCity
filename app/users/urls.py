from django.contrib import admin
from django.urls import include, path
from users import views as users_views

urlpatterns = [
    path('favorite', users_views.FavoriteView.as_view(), name='favorite'),
    path('basket', users_views.BasketView.as_view(), name='basket'),
    path('register/', users_views.register, name='register'),
    path('login/', users_views.login, name='login'),
    path('logout/', users_views.logout, name='logout'),
]
