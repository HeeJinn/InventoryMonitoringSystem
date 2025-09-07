import datetime
from math import trunc

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render

from InventoryMonitoringSystem.models import *
import json
from django.shortcuts import render
from .models import Items, Transactions
from django.db.models import Count

# Create your views here.

def index(request):
    dateNow = datetime.datetime.today()
    totalItems = Items.objects.count()
    totalSales = Transactions.objects.all()
    totalCustomers = Customer.objects.count()
    # --- NEW: Get Hit Items using Raw SQL ---
    sql_query = """
        SELECT i.item_name, COUNT(t.item_id) AS sales_count FROM transactions t JOIN items i ON t.item_id = i.item_id
        GROUP BY i.item_name
        ORDER BY sales_count DESC LIMIT 5;
    """

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        top_selling_items = cursor.fetchall()

    hitItems = len(top_selling_items)  # The number of top items (e.g., 5)
    # --- END of new logic ---
    # top_selling_items = Transactions.objects.values('item__item_name').annotate(
    #     sales_count=Count('item__item_name')
    # ).order_by('-sales_count')[:5]
    # hitItems = len(top_selling_items)
    sales = 0
    for sale in totalSales:
        sales += sale.total_amount

    context = {
        "activePage": "dashboard",
        "totalItems": totalItems,
        "totalCustomers": totalCustomers,
        "hitItems": hitItems,
        "sales": sales,
        "dateNow": dateNow
    }
    return render(request, "homeUI/index.html", context)

def costumerPage(request):
    costumers = Customer.objects.all()
    context = {
        "activePage": "customer",
        "costumers": costumers,
    }
    return render(request, "homeUI/customers.html", context)
    
def itemsPage(request):
    items = Items.objects.all()
    context = {
        "activePage": "items",
        "items": items,
    }
    return render(request, "homeUI/items.html", context)
    
def transacationsPage(request):
    transactions = Transactions.objects.all()
    context = {
        "activePage": "transactions",
        "transactions": transactions,
    }
    return render(request, "homeUI/transactions.html", context)
