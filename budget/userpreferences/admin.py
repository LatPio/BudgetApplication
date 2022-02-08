from django.contrib import admin
from .models import UserPreferences

# Register your models here.

# class ExpenseAdmin(admin.ModelAdmin):
admin.site.register(UserPreferences)

# from django.contrib import admin
# from .models import Expense, Category
#
#
# # Register your models here.
#
#
# class ExpenseAdmin(admin.ModelAdmin):
#     list_display = ('amount', 'description', 'category', 'date', 'owner')
#     search_field = ['amount']
#
#     list_per_page = 5
#
# admin.site.register(Expense, ExpenseAdmin)
# admin.site.register(Category)
