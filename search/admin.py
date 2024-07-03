from django.contrib import admin
from .models import SearchQuery

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('query', 'created_at')
    search_fields = ('query',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
