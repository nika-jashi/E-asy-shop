from django.urls import path

from apps.products.views import (ProductCreationView,
                                 ProductListView,
                                 ProductDetailView,
                                 ProductUpdateView,
                                 ProductDeleteView)

urlpatterns = [
    path('create/', ProductCreationView.as_view(), name='product-creation'),
    path('list/', ProductListView.as_view(), name='product-list'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('item/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
]
