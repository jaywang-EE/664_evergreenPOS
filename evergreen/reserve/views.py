from reserve.models import Reserve, Table, TableType

from django.views import View
from django.views import generic
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateForm
from datetime import date, datetime

from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView


class ReserveListView(LoginRequiredMixin, View) :
    def get(self, request):
        rl = Reserve.objects.all();
        d = request.GET.get('d')
        hr = int(request.GET.get('h'))
        valid_input = False
        if d and hr:
            now = datetime.now().date()
            ds = datetime.strptime(d, "%Y-%m-%d").date()
            if ds > now or (ds == now and (int(hr)) > datetime.now().hour):
                object_list = Reserve.objects.filter(
                    Q(date__icontains=ds) & Q(hour__icontains=hr) 
                )
                valid_input = True
                max_talbe_num[0] = max(max_talbe_num[0]-len(object_list), 0)
        ctx = {'reserve_list': rl};
        return render(request, 'reserves/reserve_list.html', ctx)

class ReserveDetailView(OwnerDetailView):
    model = Reserve
    template_name = "reserves/reserve_detail.html"

class ReserveCreateView(OwnerCreateView):
    model = Reserve
    form_class = CreateForm
    template_name = "reserves/reserve_form.html"

class ReserveUpdateView(OwnerUpdateView):
    model = Reserve
    fields = ['custom', 'date', 'hour']
    template_name = "reserves/reserve_form.html"

class ReserveDeleteView(OwnerDeleteView):
    model = Reserve
    template_name = "reserves/reserve_delete.html"

