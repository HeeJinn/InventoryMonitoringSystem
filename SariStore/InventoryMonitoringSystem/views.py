import dataclasses
import datetime
from math import trunc
import json

from django.core.paginator import Paginator
from django.db import connection
from django.db.models.functions import TruncMonth, TruncDay
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

    # Chart 1: Bar Chart (Monthly Sales)
    sales_per_day = Transactions.objects.annotate(
        day=TruncDay('date_added')
    ).values('day').annotate(
        total=Sum('total_amount')
    ).order_by('day')

    sales_labels = [s['day'].strftime('%b %d') for s in sales_per_day]
    sales_data = [float(s['total']) for s in sales_per_day]

    # Chart 2: Doughnut Chart (Sales by Category)
    sales_by_category = Items.objects.values('category').annotate(
        total_sold=Sum('transactions__quantity')
    ).order_by('-total_sold')

    category_labels = [c['category'] for c in sales_by_category if c['category']]  # Added check for null category
    category_data = [int(c['total_sold']) for c in sales_by_category if c['category']]

    # Chart 3: Line Chart (Cumulative Sales Growth)
    daily_sales = Transactions.objects.annotate(
        day=TruncDay('date_added')
    ).values('day').annotate(
        daily_total=Sum('total_amount')
    ).order_by('day')

    cumulative_sales_labels = []
    cumulative_sales_data = []
    running_total = 0
    for sale in daily_sales:
        running_total += sale['daily_total']
        cumulative_sales_labels.append(sale['day'].strftime('%b %d'))
        cumulative_sales_data.append(float(running_total))

    context = {
        "activePage": "dashboard",
        "totalItems": totalItems,
        "totalCustomers": totalCustomers,
        "hitItems": hitItems,
        "sales": sales,
        "dateNow": dateNow,

        'sales_labels': json.dumps(sales_labels),
        'sales_data': json.dumps(sales_data),
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
        'cumulative_sales_labels': json.dumps(cumulative_sales_labels),
        'cumulative_sales_data': json.dumps(cumulative_sales_data),
    }
    return render(request, "homeUI/index.html", context)

def customerPage(request):
    customers = Customer.objects.all()
    searchQuery = request.GET.get("search")
    if searchQuery:
        customers = Customer.objects.filter(Q(first_name__icontains=searchQuery) | Q(last_name__icontains=searchQuery))
    paginator = Paginator(customers, 10)
    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)
    context = {
        "activePage": "customer",
        "customers": customers,
        "search": searchQuery,
        "pageObj": pageObj
    }
    return render(request, "homeUI/customers.html", context)
    
def itemsPage(request):
    searchFields = ["item_name__icontains", "category__icontains"]
    searchQuery = request.GET.get("search")
    items = searchModels(Items, searchQuery, searchFields)
    paginator = Paginator(items, 10)
    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)
    context = {
        "activePage": "items",
        "pageObj": pageObj,
        "search": searchQuery
    }
    return render(request, "homeUI/items.html", context)
    
def transacationsPage(request):
    searchQuery = request.GET.get('search')
    transactions = Transactions.objects.all()
    if searchQuery:
        transactions = Transactions.objects.filter(
            Q(customer__first_name__icontains=searchQuery) |
            Q(customer__last_name__icontains=searchQuery) |
            Q(customer__contact_number__icontains=searchQuery) |
            Q(item__item_name__icontains=searchQuery)
        )
    paginator = Paginator(transactions, 10)
    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)

    context = {
        "activePage": "transactions",
        "pageObj": pageObj,
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
