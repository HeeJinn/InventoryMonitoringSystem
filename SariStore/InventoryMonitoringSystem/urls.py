from django.urls import path

from InventoryMonitoringSystem import views

urlpatterns = [
    path("dashboard/", views.index, name="dashboard"),
    path("customer/", views.customerPage, name="customer"),
    path("items/", views.itemsPage, name="items"),
    path("transactions/", views.transacationsPage, name="transactions"),

]