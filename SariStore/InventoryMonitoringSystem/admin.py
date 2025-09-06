from django.contrib import admin

from InventoryMonitoringSystem.models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Items)
admin.site.register(Transactions)
