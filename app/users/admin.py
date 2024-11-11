from django.contrib import admin
from users import models as user_models


@admin.register(user_models.CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
    )

    search_fields = (
        'id',
        'email',
    )

    readonly_fields = (
    )
