from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # Перемикач мови
    path("rosetta/", include("rosetta.urls")),
]

# Локалізовані маршрути
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("catalog.urls")),  # Додаток Catalog
    path("", include("info.urls")),  # Додаток Info
    path("user/", include("users.urls")),  # Додаток Users
    path("ckeditor5/", include("django_ckeditor_5.urls")),  # Підключення CKEditor 5
    prefix_default_language=False,  # Не додавати суфікс для мови за замовчуванням
)

# Додаткові маршрути в режимі DEBUG
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
