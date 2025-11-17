from django.contrib import admin
from .models import Budget

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'spent', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['category', 'user__username']






