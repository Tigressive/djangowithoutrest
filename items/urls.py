from django.urls import path, include

import items.api_views
from . import views
from . import api_views

urlpatterns = [
    path('items', views.ItemListView.as_view(), name="items.list"),
    path('items/<int:pk>', views.ItemDetailView.as_view(), name="items.detail"),
    path('items/<int:pk>/edit', views.ItemUpdateView.as_view(), name="items.update"),
    path('items/<int:pk>/delete', views.ItemDeleteView.as_view(), name="items.delete"),
    path('items/new', views.ItemCreateView.as_view(), name="items.new"),



]
