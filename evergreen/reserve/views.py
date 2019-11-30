from reserve.models import Reserve, Table, TableType

from django.views import View
from django.views import generic
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateForm
from django import forms
from datetime import date, datetime, timedelta
from django.utils import timezone
import pytz


from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView


class ReserveListView(LoginRequiredMixin, View) :
    def get(self, request):
        now = timezone.now()
        rl = Reserve.objects.filter(date__gte=now).filter(owner=self.request.user).order_by('date', 'hour');
        tl = [i for i in range(11, 21)]
        tm = request.GET.get('d')
        table_name = request.GET.get('n')
        err_msg = ""
        tb_list = []
        tm_str = ""
        if tm:
            timezone.activate(pytz.timezone('US/Michigan'))
            tm = timezone.make_aware(datetime.strptime(tm, "%Y/%m/%d %H:%M"))
            try:
                if tm<=now:
                    err_msg="No past time!"
                elif tm > (now+timedelta(days=7)):
                    err_msg="We only accept booking in 1 week!"
                elif 10<tm.hour<21:
                    object_list = Reserve.objects.filter(
                        Q(date__icontains=tm.strftime("%Y-%m-%d")) & Q(hour__icontains=tm.hour)
                    )
                    object_list = [obj.table for obj in object_list]
                    for tb in Table.objects.all().order_by('category', 'name'):
                        print(tb)
                        tb_list.append((tb, (tb not in object_list)))
                    tm_str = tm.strftime("%Y/%m/%d-%H:%M")
                else:
                    err_msg="We open in 11:00~20:00"
            except: 
                err_msg="Illegal input!"

        ctx = {'reserve_list': rl, 'err_msg': err_msg, 'tb_list': tb_list, 
               'time_list':tl, 'tm':tm_str};
        return render(request, 'reserves/reserve_list.html', ctx)

class ReserveDetailView(OwnerDetailView):
    model = Reserve
    template_name = "reserves/reserve_detail.html"

class ReserveCreateView(OwnerCreateView):
    model = Reserve
    form_class = CreateForm
    template_name = "reserves/reserve_form.html"

    def form_valid(self, form):
        print("fv")
        object = form.save(commit=False)
        dh = datetime.strptime(self.request.GET.get('d'), "%Y/%m/%d-%H:%M")
        object.custom = str(self.request.user)
        object.table = Table.objects.get(id=self.request.GET.get('n'))
        object.date = dh.strftime("%Y-%m-%d")
        object.hour = dh.hour
        return super(ReserveCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super( ReserveCreateView, self).get_form_kwargs()
        # update the kwargs for the form init method with yours
        print((kwargs))
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        return kwargs

    def get_initial(self):
        initial = super(ReserveCreateView, self).get_initial()

        initial['table'] = Table.objects.get(id=self.request.GET.get('n'))

        return initial

class ReserveUpdateView(OwnerUpdateView):
    model = Reserve
    fields = ['custom', 'date', 'hour']
    template_name = "reserves/reserve_form.html"

class ReserveDeleteView(OwnerDeleteView):
    model = Reserve
    template_name = "reserves/reserve_delete.html"

