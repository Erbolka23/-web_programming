from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'starts_at', 'is_published', 'created_at')
    list_filter = ('is_published', 'starts_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Event, EventAdmin)
