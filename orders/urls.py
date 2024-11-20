from django.urls import path
from .views import new_quick_order, new_order, OrderListView, OrderDetailView

# orders_list, order_detail
urlpatterns = [
    path('new/', new_order, name="new_order"),
    path('new/quick/', new_quick_order, name="new_quick_order"),
    path('list/', OrderListView.as_view(), name="orders"),
    path('detail/<str:number>/', OrderDetailView.as_view(), name="order_detail"),
    # path('list/', orders_list, name="orders"),
    # path('detail/<str:number>/', order_detail, name="order_detail"),
]