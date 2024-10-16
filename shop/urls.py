from django.urls import path
from .views import (ProductListView, ProductCreateView, ProductDetailView, ProductUpdateView, ProductDeleteView,
                    CategoryCreateView, CategoryListView, CategoryDetailView, CategoryUpdateView, CategoryDeleteView)

app_name = 'shop'

urlpatterns = [
    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/update/<slug:slug>/', ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<slug:slug>/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/', ProductListView.as_view(), name='products'),


    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('categories/update/<slug:slug>/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<slug:slug>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('categories/', CategoryListView.as_view(), name='categories'),
]
