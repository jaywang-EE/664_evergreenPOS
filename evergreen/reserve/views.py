from reserve.models import Reserve, Table, TableType

from django.views import View
from django.views import generic
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from datetime import datetime, timedelta

from home.owner import OwnerListView, OwnerCreateView, OwnerDeleteView
from .forms import CreateForm

from evergreen.timezone import ttos, stot

class ReserveListView(LoginRequiredMixin, View) :
    def get(self, request):
        tm = request.GET.get('d')
        now = datetime.now()
        rl = Reserve.objects.filter(time__gte=now).filter(owner=self.request.user).order_by("time");
        #init
        err_msg = ""
        tm_str = ""
        tb_list = []
        if tm:
            tm = stot(tm)
            try:
                if tm<=now:
                    err_msg="No past time!"
                elif tm > (now+timedelta(days=7)):
                    err_msg="We only accept booking in 1 week!"
                elif 10<tm.hour<21:
                    table_list = [obj.table for obj in Reserve.objects.filter(time=tm)]
                    for tb in Table.objects.all().order_by('category', 'name'):
                        tb_list.append((tb, (tb not in table_list)))
                    tm_str = ttos(tm)
                else:
                    err_msg="We open in 11:00~20:00"
            except: 
                err_msg="Illegal input!"

        ctx = {'reserve_list': rl, 'err_msg': err_msg, 'tb_list': tb_list, 
               'time_list':[i for i in range(11, 21)], 'tm':tm_str};
        return render(request, 'reserves/reserve_list.html', ctx)

class ReserveCreateView(OwnerCreateView):
    model = Reserve
    form_class = CreateForm
    template_name = "reserves/reserve_form.html"

    def get_context_data(self, **kwargs): # visual
        ctx = super(ReserveCreateView, self).get_context_data(**kwargs)
        ctx['date'], ctx['hour'] = self.request.GET.get('d').split('-')
        ctx['table_type'] = str(Table.objects.get(id=self.request.GET.get('n')).category)
        return ctx

    def form_valid(self, form):
        object = form.save(commit=False)
        object.custom = str(self.request.user)
        object.table  = Table.objects.get(id=self.request.GET.get('n'))
        object.time   = stot(self.request.GET.get('d'))
        return super(ReserveCreateView, self).form_valid(form)
    
    def get_initial(self):
        initial = super(ReserveCreateView, self).get_initial()
        initial['table'] = Table.objects.get(id=self.request.GET.get('n'))
        return initial
    
class ReserveDeleteView(OwnerDeleteView):
    model = Reserve
    template_name = "reserves/reserve_delete.html"

