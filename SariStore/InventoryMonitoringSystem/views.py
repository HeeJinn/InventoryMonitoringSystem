from django.http import HttpResponse
from django.shortcuts import render

from InventoryMonitoringSystem.models import *


# Create your views here.

def index(request):
    totalItems = len(Items.objects.all())
    totalSales = Transactions.objects.all()
    sales = 0
    for sale in totalSales:
        sales += sale.total_amount

    context = {
        "totalItems": totalItems,
        "totalSales": totalSales,
        "sales": sales,
    }
    return render(request, "homeUI/index.html", context)
