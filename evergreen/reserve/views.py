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
        table_name = request.GET.get('n')
        err_msg = ""
        tb_list = []
        tm_str = ""
        if tm:
            try:
                now = datetime.now()
                tm = datetime.strptime(tm, "%Y/%m/%d %H:%M")
                #try:
                if tm>now:
                    print('LG')
                    object_list = Reserve.objects.filter(
                        Q(date__icontains=tm.strftime("%Y-%m-%d")) & Q(hour__icontains=tm.hour)
                    )

                    tb_dict = {}
                    for tb in Table.objects.all():
                        tb_dict[tb] = True
                    for res in Reserve.objects.all():
                        tb_dict[res.table] = False
                    for tb, val in tb_dict.items():
                        tb_list.append(("%s_%s"%(tb.category.name, tb.name), tb.id, val))
                    tm_str = tm.strftime("%Y-%m-%d-%H")
                else:
                    print(tm.strftime("%Y/%m/%d %H:%M"))
                    print("NOW",now.strftime("%Y/%m/%d %H:%M"))
                    err_msg="No past time!"
            except: 
                err_msg="Illegal input!"
        else: err_msg = "Select your prefered time."

        ctx = {'reserve_list': rl, 'err_msg': err_msg, 'tb_list': tb_list, 
               'time_list':tl, 'tm':tm_str,};
        return render(request, 'reserves/reserve_list.html', ctx)

class ReserveDetailView(OwnerDetailView):
    model = Reserve
    template_name = "reserves/reserve_detail.html"

class ReserveCreateView(OwnerCreateView):
    model = Reserve
    form_class = CreateForm
    template_name = "reserves/reserve_form.html"

    def form_valid(self, form):
        print('form_valid called')
        print(str(self.request.user))
        return super(ReserveCreateView, self).form_valid(form)

    def get_initial(self, *args, **kwargs):
        initial = super(ReserveCreateView, self).get_initial(**kwargs)
        #['custom', 'date', 'hour', 'person', 'table']
        dh = datetime.strptime(self.request.GET.get('d'), "%Y-%m-%d-%H")
        initial['custom'] = str(self.request.user)
        initial['table'] = Table.objects.get(id=self.request.GET.get('n'))
        initial['date'] = dh.strftime("%Y-%m-%d")
        initial['hour'] = dh.hour
        return initial

class ReserveUpdateView(OwnerUpdateView):
    model = Reserve
    fields = ['custom', 'date', 'hour']
    template_name = "reserves/reserve_form.html"

class ReserveDeleteView(OwnerDeleteView):
    model = Reserve
    template_name = "reserves/reserve_delete.html"

