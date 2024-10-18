from django.urls import path
from .views import (ProductListView, ProductCreateView, ProductDetailView, ProductUpdateView, ProductDeleteView,
                    CategoryCreateView, CategoryListView, CategoryDetailView, CategoryUpdateView, CategoryDeleteView,
                    IndexTemplateView, ProductListByCategory, product_search)

app_name = 'shop'

urlpatterns = [

    path('', IndexTemplateView.as_view(), name='index'),
    path('search/', product_search, name='product_search'),


    path('categories/<slug:slug>/products/', ProductListByCategory.as_view(), name='products_by_category'),
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
