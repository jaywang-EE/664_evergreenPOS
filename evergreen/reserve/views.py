from reserve.models import Reserve

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
        max_talbe_num = [10, 4]
        query = request.GET.get('q')
        rl = Reserve.objects.all();
        if not query: max_talbe_num[0] =  -1
        else:
            querys = query.split('.')
            if len(querys) == 2:
                now = datetime.now().date()
                ds, hr = querys
                d = datetime.strptime(ds, "%Y-%m-%d").date()
                print(datetime.now().hour)
                if d > now or (d == now and (int(hr)+12) > datetime.now().hour):
                    object_list = Reserve.objects.filter(
                        Q(date__icontains=ds) & Q(hour__icontains=hr) 
                    )
                    max_talbe_num[0] = max(max_talbe_num[0]-len(object_list), 0)
                else:
                    max_talbe_num[0] = -3
            else:
                max_talbe_num[0] = -2
                #object_list = Reserve.objects.filter(Q(hour__icontains=-1))
        ctx = { 'rest_small': max_talbe_num[0], 
                'rest_big': max_talbe_num[1], 
                'reserve_list': rl};
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

