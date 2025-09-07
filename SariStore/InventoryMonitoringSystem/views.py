import datetime
from math import trunc

from django.db import connection
from django.http import HttpResponse

from InventoryMonitoringSystem.models import *
from django.shortcuts import render
from .models import Items, Transactions
from django.db.models import Q

# Create your views here.

def index(request):
    dateNow = datetime.datetime.today()
    totalItems = Items.objects.count()
    totalSales = Transactions.objects.all()
    totalCustomers = Customer.objects.count()

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

def customerPage(request):
    customers = None
    search = request.GET.get("search")
    if search:
        customers = Customer.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search))
    else:
        customers = Customer.objects.all()

    context = {
        "activePage": "customer",
        "customers": customers,
        "search": search
    }
    return render(request, "homeUI/customers.html", context)
    
def itemsPage(request):
    searchFields = ["item_name__icontains", "category__icontains"]
    searchQuery = request.GET.get("search")
    items = searchModels(Items, searchQuery, searchFields)
    context = {
        "activePage": "items",
        "items": items,
        "search": searchQuery
    }
    return render(request, "homeUI/items.html", context)
    
def transacationsPage(request):
    searchQuery = request.GET.get('search')

    if searchQuery:
        transactions = Transactions.objects.filter(
            Q(customer__first_name__icontains=searchQuery) |
            Q(customer__last_name__icontains=searchQuery) |
            Q(customer__contact_number__icontains=searchQuery) |
            Q(item__item_name__icontains=searchQuery)
        )
    else:
        transactions = Transactions.objects.all()

    context = {
        "activePage": "transactions",
        "transactions": transactions,
        "search": searchQuery
    }
    return render(request, "homeUI/transactions.html", context)


def searchModels(model, query, searchFields):
    if not query:
        return model.objects.all()
    q_objects = Q()
    for field in searchFields:
        q_objects |= Q(**{field: query})
    return model.objects.filter(q_objects)
