from django.views.generic import (ListView, CreateView,
                                  UpdateView, DetailView,
                                  DeleteView, TemplateView)
from django.core.paginator import Paginator

from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Product, Category
from .forms import CategoryCreateForm, ProductCreateForm
from .filters import ProductFilter
from django.contrib.auth import get_user_model




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
    paginate_by = 3  # Количество продуктов на странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        context['filterset'] = self.filterset
        context['current_page'] = 'shop:products'

        return context

    def get_queryset(self):
        if not self.kwargs.get('slug'):
            queryset = Product.objects.all()
        else:
            # Получаем категорию по slug из URL
            category = get_object_or_404(Category, slug=self.kwargs['slug'])
            queryset = Product.objects.filter(category=category)

        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(Q(name__icontains=query))

        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = 'categories'
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'shop/admin/categories.html'
    context_object_name = 'categories'

    def get_template_names(self):
        user = get_user_model()
        admin = user.objects.get(username='staff')
        if self.request.user == admin:
            return ['shop/admin/categories.html']
        else:
            return ['shop/categories.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'shop:categories'

        return context


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    slug_url_kwarg = 'slug'

    def get_template_names(self):
        user = get_user_model()
        admin = user.objects.get(username='staff')
        if self.request.user == admin:
            return ['shop/admin/category_detail.html']
        else:
            return ['shop/category_detail.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        products = category.products.all()[:2]
        context['products'] = products

        return context


def about(request):
    context = {
        'name': 'Книжный',
        'type': '---ИНТЕРНЕТ-МАГАЗИН---',
        'city': 'Санкт-Петербург',
        'year': '2024',
        'pr_name': 'Алина',
        'pr_lastname': 'Бурлова',
        'pr_email': 'alina-burlova@bk.ru',
        'current_page': 'shop:about',
    }

    return render(request, template_name='shop/about.html', context=context)


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
    queryset = Product.objects.all()

    if query:
        queryset = queryset.filter(Q(name__icontains=query))

    filterset = ProductFilter(request.GET, queryset)

    results = filterset.qs
    categories = Category.objects.all()

    paginator = Paginator(results, 3)
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'page_obj': page_obj,
        'filterset': filterset,
        'is_paginated': paginator.num_pages > 1,
        'query': query,
        'current_page': 'shop:products',
    }

    return render(request, template_name="shop/products_by_category.html", context=context)


# def product_list_view(request, slug):
#     categories = Category.objects.all()
#     if slug:
#         category = get_object_or_404(Category, slug=slug)
#         products_by_category = Product.objects.filter(category=category)
#         filterset = ProductFilter(request.GET, queryset=products_by_category)
#         context = {"products": filterset.qs, 'filterset': filterset, "categories": categories}
#         return render(request, template_name="shop/products_by_category.html", context=context)
#
#     queryset = Product.objects.all()
#     filterset = ProductFilter(request.GET, queryset=queryset)
#     context = {"products": filterset.qs, 'filterset': filterset, "categories": categories}
#
#     return render(request, template_name="shop/products_by_category.html", context=context)

def forbidden(request, exception):
    return render(request, "403.html", status=403)


def page_not_found(request, exception):
    return render(request, "404.html", status=404)


def server_error(request):
    return render(request, "500.html", status=500)

