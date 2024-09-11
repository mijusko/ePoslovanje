from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from api.models import User, SavedMovie

# Prilagođeni UserAdmin za vaš model User


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'profile_picture')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture',)}),
    )


# Registrujte prilagođeni User model u admin panelu
admin.site.register(User, UserAdmin)

# Registrujte SavedMovie model u admin panelu


@admin.register(SavedMovie)
class SavedMovieAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie_id', 'saved_at')
    search_fields = ('user__username', 'movie_id')
    ordering = ('-saved_at',)
