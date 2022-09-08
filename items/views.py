from django.shortcuts import render
from django.http import Http404
from django.views.generic import CreateView, DetailView, ListView

from .forms import ItemsForm
from .models import Items


class ItemCreateView(CreateView):
    model = Items
    success_url = '/item/items'
    form_class = ItemsForm


class ItemListView(ListView):
    model = Items
    context_object_name = "items"
    template_name = "items/items_list.html"


class ItemDetailView(DetailView):
    model = Items
    context_object_name = "item"
    template_name = "items/items_detail.html"
# Create your views here.
