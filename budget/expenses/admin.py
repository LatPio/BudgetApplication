from django.contrib import admin
from .models import Expense, Category, Budynek


# Register your models here.


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'waluta', 'budynek', 'description', 'category', 'date', 'owner')
    search_fields = ['amount', 'budynek', 'waluta', 'description', 'category', 'date',]

    list_per_page = 20
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')

class BudynekAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Budynek, BudynekAdmin)



