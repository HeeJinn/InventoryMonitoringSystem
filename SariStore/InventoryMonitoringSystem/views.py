
import datetime
from math import trunc
import json

from django.core.paginator import Paginator
from django.db import connection
from django.db.models.functions import  TruncDay, TruncWeek
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

    category_labels = [c['category'] for c in sales_by_category if c['category']]
    category_data = [int(c['total_sold']) for c in sales_by_category if c['category']]

    # CHART 3: LINE CHART (Weekly Sales Trend)

    weekly_sales = Transactions.objects.annotate(
        week=TruncWeek('date_added')
    ).values('week').annotate(
        weekly_total=Sum('total_amount')
    ).order_by('week')

    weekly_sales_labels = [sale['week'].strftime('Week of %b %d') for sale in weekly_sales]
    weekly_sales_data = [float(sale['weekly_total']) for sale in weekly_sales]

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
        'weekly_sales_labels': json.dumps(weekly_sales_labels),
        'weekly_sales_data': json.dumps(weekly_sales_data),
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

    transactions_list = Transactions.objects.select_related('customer', 'item')

    if searchQuery:
        transactions_list = transactions_list.filter(
            Q(customer__first_name__icontains=searchQuery) |
            Q(customer__last_name__icontains=searchQuery) |
            Q(customer__contact_number__icontains=searchQuery) |
            Q(item__item_name__icontains=searchQuery)
        )

    paginator = Paginator(transactions_list, 10)
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
