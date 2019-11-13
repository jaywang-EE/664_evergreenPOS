from django.urls import path, reverse_lazy
from . import views

app_name='reserves'
urlpatterns = [
    path('', views.ReserveListView.as_view(), name='all'),
    path('reserves/<int:pk>', views.ReserveDetailView.as_view(), name='reserve_detail'),
    path('reserves/create', 
        views.ReserveCreateView.as_view(success_url=reverse_lazy('reserves:all')), name='reserve_create'),
    path('reserves/<int:pk>/update', 
        views.ReserveUpdateView.as_view(success_url=reverse_lazy('reserves:all')), name='reserve_update'),
    path('reserves/<int:pk>/delete', 
        views.ReserveDeleteView.as_view(success_url=reverse_lazy('reserves:all')), name='reserve_delete'),
]

# We use reverse_lazy in urls.py to delay looking up the view until all the paths are defined
