"""wheresmystuff URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

import items.api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('item/', include('items.urls')),
    path('api/v1/items/', items.api_views.ItemList.as_view()),
    path('api/v1/items/new', items.api_views.ItemCreation.as_view()),
    path('api/v1/items/<int:id>/', items.api_views.ItemRetrieveUpdateDestroy.as_view()),
    path('api/v1/items/<int:id>/borrow', items.api_views.BorrowItem.as_view()),
    path('api/v1/items/auth', items.api_views.AuthenticateView.as_view()),
    path('api/v1/items/authtoken', obtain_auth_token),
    path('api/v1/items/myItems', items.api_views.UserItemList.as_view()),
    path('api/v1/users/', items.api_views.UserList.as_view()),
    path('api/v1/users/<int:id>/', items.api_views.UserRetrieveUpdateDestroy.as_view()),
    path('api/v1/users/getByUsername/<str:username>', items.api_views.UserRetrieveUpdateDestroy.as_view())
]
