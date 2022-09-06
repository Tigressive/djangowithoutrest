from django.urls import path, include

from . import views

urlpatterns = [
    path('items', views.list),
    path('items/<int:pk>', views.detail),

]