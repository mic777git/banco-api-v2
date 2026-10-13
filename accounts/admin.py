from django.contrib import admin
from .models import Account, Transaction


class TransactionInline(admin.TabularInline):
    model = Transaction
    fk_name = 'account'
    extra = 0


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance', 'created_at')
    inlines = [TransactionInline]


admin.site.register(Transaction)