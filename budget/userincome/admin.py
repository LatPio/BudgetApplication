from django.contrib import admin
from .models import UserIncome, Source

from .models import Budynek


class UserIncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'waluta', 'budynek', 'description', 'source', 'date', 'owner')
    search_fields = ['amount', 'budynek', 'waluta', 'description', 'source', 'date']

    list_per_page = 20


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')



# class BudynekAdmin(admin.ModelAdmin):
#     list_display = ('name', 'owner')


admin.site.register(UserIncome, UserIncomeAdmin)
admin.site.register(Source, SourceAdmin)
# admin.site.register(Budynek, BudynekAdmin)