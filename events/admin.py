from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_published', 'created_at')
    list_filter = ('is_published', 'date')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Event, EventAdmin)
