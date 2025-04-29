from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created']
    list_filter = ['status', 'created']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created', 'updated']
    fieldsets = [
        (None, {'fields': ['name', 'email', 'phone', 'subject', 'message']}),
        ('Statut', {'fields': ['status', 'reply']}),
        ('Dates', {'fields': ['created', 'updated'], 'classes': ['collapse']}),
    ]
