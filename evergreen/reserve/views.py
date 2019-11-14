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
        tl = [i for i in range(11, 21)]
        tm = request.GET.get('d')
        err_msg = ""
        tb_list = []
        val_list = []
        if tm:
            #try:
            now = datetime.now()
            tm = datetime.strptime(tm, "%Y/%m/%d %H:%M")
            if tm>now:
                print(tm.strftime("%Y-%m-%d"))
                object_list = Reserve.objects.filter(
                    Q(date__icontains=tm.strftime("%Y-%m-%d")) & Q(hour__icontains=tm.hour)
                )

                tb_dict = {}
                for tb in Table.objects.all():
                    tb_dict[tb] = True
                for res in Reserve.objects.all():
                    tb_dict[res.table] = False
                tb_list = list(tb_dict.items())
                val_list = list(tb_dict.values())
            else:
                err_msg="No past time!"
            '''
            except: 
                err_msg="Illegal input!"
            '''
        else: err_msg = "Select your prefered time."

        ctx = {'reserve_list': rl, 'err_msg': err_msg, 'tb_list': tb_list, 'val_list': val_list, 'time_list':tl};
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

