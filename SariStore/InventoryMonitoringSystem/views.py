import datetime
from math import trunc
import json

from django.db import connection
from django.db.models.functions import TruncMonth
from django.http import HttpResponse

from InventoryMonitoringSystem.models import *
from django.shortcuts import render
from .models import Items, Transactions
from django.db.models import Q, Count, Sum


# Create your views here.

def index(request):
    dateNow = datetime.datetime.today()
    totalItems = Items.objects.count()
    totalSales = Transactions.objects.all()
    totalCustomers = Customer.objects.count()
    top_selling_items = Transactions.objects.values('item__item_name').annotate(
        sales_count=Count('item__item_name')).order_by('-sales_count')[:5]
    hitItems = len(top_selling_items)
    sales = 0
    for sale in totalSales:
        sales += sale.total_amount

    # --- ADD THIS: Data queries for your charts ---
    # Chart 1: Bar Chart (Monthly Sales)
    sales_per_month = Transactions.objects.annotate(
        month=TruncMonth('transaction_date')
    ).values('month').annotate(
        total=Sum('total_amount')
    ).order_by('month')

    sales_labels = [s['month'].strftime('%B') for s in sales_per_month]
    sales_data = [float(s['total']) for s in sales_per_month]

    # Chart 2: Doughnut Chart (Sales by Category)
    sales_by_category = Items.objects.values('category').annotate(
        total_sold=Sum('transactions__quantity')
    ).order_by('-total_sold')

    category_labels = [c['category'] for c in sales_by_category if c['category']]  # Added check for null category
    category_data = [int(c['total_sold']) for c in sales_by_category if c['category']]

    # Chart 3: Line Chart (New Customers per Month)
    customers_per_month = Customer.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('customer_id')
    ).order_by('month')

    customer_labels = [c['month'].strftime('%B') for c in customers_per_month]
    customer_data = [c['count'] for c in customers_per_month]
    # --- End of new code section ---

    context = {
        "activePage": "dashboard",
        "totalItems": totalItems,
        "totalCustomers": totalCustomers,
        "hitItems": hitItems,
        "sales": sales,
        "dateNow": dateNow,

        # ADD THESE LINES to your context dictionary
        'sales_labels': json.dumps(sales_labels),
        'sales_data': json.dumps(sales_data),
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
        'customer_labels': json.dumps(customer_labels),
        'customer_data': json.dumps(customer_data),
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
