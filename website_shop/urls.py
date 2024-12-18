"""
URL configuration for website_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from shop.views import AdminTemplateView, ProductListByCategory
from website_shop import settings
from orders.views import all_order_list

urlpatterns = [
    path('staff/orders/', all_order_list, name="admin_all_orders"),
    path('staff/', AdminTemplateView.as_view(), name="admin-page"),
    path('admin/', admin.site.urls),
    path('products/', include('shop.urls')),
    path('users/', include('users.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('', ProductListByCategory.as_view(), name='main'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = "shop.views.forbidden"
handler404 = "shop.views.page_not_found"
handler500 = "shop.views.server_error"
