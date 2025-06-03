from django.contrib import admin

from users.models import User

# Чтобы была возможность редактировать пароли через админку,
# наследуйся от from django.contrib.auth.admin import UserAdmin.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    list_editable = ('role',)
