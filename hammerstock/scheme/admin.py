from django.contrib import admin
from .models import SchemeCustomer, Deposit, DepositReceipt

# Register your models here.

admin.site.register(SchemeCustomer)
admin.site.register(Deposit)
admin.site.register(DepositReceipt)
# we are simply telling django to show records so that I can manage them from the browser