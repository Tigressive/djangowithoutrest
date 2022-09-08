from django.urls import path, include

from . import views

urlpatterns = [
    path('items', views.ItemListView.as_view(), name="items.list"),
    path('items/<int:pk>', views.ItemDetailView.as_view(), name="items.detail"),
    path('items/new', views.ItemCreateView.as_view(), name="items.new")
]
