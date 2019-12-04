from django.urls import path, reverse_lazy
from . import views

app_name='orders'
urlpatterns = [
    path('', views.OrderListView.as_view(), name='all'),
    path('orders/create', 
        views.OrderCreateView.as_view(success_url=reverse_lazy('orders:all')), name='order_create'),
    path('orders/<int:pk>/delete', 
        views.OrderDeleteView.as_view(success_url=reverse_lazy('orders:all')), name='order_delete'),
]

# We use reverse_lazy in urls.py to delay looking up the view until all the paths are defined
