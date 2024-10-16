from django.views.generic import (ListView, CreateView,
                                  UpdateView, DetailView,
                                  DeleteView, TemplateView)

from django.urls import reverse_lazy

from .models import Product, Category
from .forms import CategoryCreateForm, ProductCreateForm


class AdminTemplateView(TemplateView):
    template_name = 'shop/admin.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['total'] = 5
    #     return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'shop/product_add.html'
    success_url = reverse_lazy('shop:products')


class ProductListView(ListView):
    model = Product
    template_name = 'shop/products.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = ('shop/product_detail.html')
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'shop/product_update.html'
    fields = ["category", "name", "description", "image", "price", "available"]
    success_url = reverse_lazy('shop:products')
    slug_url_kwarg = 'slug'


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shop/product_delete.html'
    success_url = reverse_lazy('shop:products')
    slug_url_kwarg = 'slug'


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'shop/category_add.html'
    success_url = reverse_lazy('shop:categories')


class CategoryListView(ListView):
    model = Category
    template_name = 'shop/categories.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'shop/category_detail.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'shop/category_update.html'
    fields = ["name"]
    success_url = reverse_lazy('shop:categories')
    slug_url_kwarg = 'slug'


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'shop/category_delete.html'
    success_url = reverse_lazy('shop:categories')
    slug_url_kwarg = 'slug'
