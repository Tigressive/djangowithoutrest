from django.shortcuts import render

from .models import Items


# Create your views here.
def list(request):
    all_items = Items.objects.all()
    return render(request, 'items/items_list.html', {'items': all_items})


def detail(request, pk):
    item = Items.objects.get(pk=pk)
    return render(request, 'items/items_detail.html', {'item': item})
