from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DetailView,
                                  DeleteView, TemplateView)

from django.urls import reverse_lazy

from .models import Product, Category
from .forms import CategoryCreateForm, ProductCreateForm


class AdminTemplateView(TemplateView):
    template_name = 'shop/admin/admin.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['total'] = 5
    #     return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'shop/admin/product_add.html'
    success_url = reverse_lazy('shop:products')


class ProductListView(ListView):
    model = Product
    template_name = 'shop/admin/products.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = ('shop/admin/product_detail.html')
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'shop/admin/product_update.html'
    fields = ["category", "name", "description", "image", "price", "available"]
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
    template_name = 'shop/admin/category_update.html'
    fields = ["name"]
    success_url = reverse_lazy('shop:categories')
    slug_url_kwarg = 'slug'


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'shop/admin/category_delete.html'
    success_url = reverse_lazy('shop:categories')
    slug_url_kwarg = 'slug'


class IndexTemplateView(TemplateView):
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        products = Product.objects.all()
        context['categories'] = categories
        context['products'] = products

        return context

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
        # Получаем категории по slug из url
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=category)


def product_search(request):
    query = request.GET.get('query')
    query_text = Q(name__icontains=query)

    results = Product.objects.filter(name=query_text)
    categories = Category.objects.all()

    context = {'categories': categories, 'products': results}

    return render(request, template_name="shop/index.html", context=context)


