from django.urls import path

from InventoryMonitoringSystem import views

urlpatterns = [
    path("home/", views.index, name="home")
]