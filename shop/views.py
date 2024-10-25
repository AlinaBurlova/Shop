from django.views.generic import (ListView, CreateView,
                                  UpdateView, DetailView,
                                  DeleteView, TemplateView)

from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Product, Category
from .forms import CategoryCreateForm, ProductCreateForm


class AdminTemplateView(TemplateView):
    template_name = 'shop/admin/admin.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['total'] = 5
    #     return context



class ProductListByCategory(ListView):
    model = Product
    template_name = 'shop/products_by_category.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories

        return context

    def get_queryset(self):
        if not self.kwargs.get('slug'):
            return Product.objects.all()

        # Получаем категорию по slug из URL
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=category)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'shop/admin/product_add.html'
    success_url = reverse_lazy('shop:products')


class ProductDetailView(DetailView):
    model = Product
    template_name = ('shop/admin/product_detail.html')
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class ProductListView(ListView):
    model = Product
    template_name = 'shop/admin/products.html'
    context_object_name = 'products'


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'shop/admin/product_edit.html'
    form_class = ProductCreateForm
    # fields = ["category", "name", "description", "image", "price", "available"]
    success_url = reverse_lazy('shop:products')
    slug_url_kwarg = 'slug'


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shop/admin/product_delete.html'
    success_url = reverse_lazy('shop:products')
    slug_url_kwarg = 'slug'


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'shop/admin/category_add.html'
    success_url = reverse_lazy('shop:categories')


class CategoryListView(ListView):
    model = Category
    template_name = 'shop/admin/categories.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'shop/admin/category_detail.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'shop/admin/category_edit.html'
    form_class = CategoryCreateForm
    # fields = ["name"]
    success_url = reverse_lazy('shop:categories')
    slug_url_kwarg = 'slug'


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'shop/admin/category_delete.html'
    success_url = reverse_lazy('shop:categories')
    slug_url_kwarg = 'slug'


def product_search(request):
    query = request.GET.get('query')
    query_text = Q(name__contains=query)

    results = Product.objects.filter(query_text)
    categories = Category.objects.all()

    context = {'categories': categories, 'products': results}

    return render(request, template_name="shop/products_by_category.html", context=context)


