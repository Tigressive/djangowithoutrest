from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView

from .forms import ItemsForm
from .models import Items


class ItemDeleteView(DeleteView):
    model = Items
    success_url = '/item/items'
    template_name = "items/items_delete.html"


class ItemUpdateView(UpdateView):
    model = Items
    success_url = '/item/items'
    form_class = ItemsForm


class ItemCreateView(CreateView):
    model = Items
    success_url = '/item/items'
    form_class = ItemsForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ItemListView(LoginRequiredMixin, ListView):
    model = Items
    context_object_name = "items"
    template_name = "items/items_list.html"
    login_url = "/admin"

    def get_queryset(self):
        return self.request.user.items.all()


class ItemDetailView(DetailView):
    model = Items
    context_object_name = "item"
    template_name = "items/items_detail.html"
# Create your views here.
