from reserve.models import Reserve, Table, TableType

from django.views import View
from django.views import generic
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateForm
from django import forms
from datetime import date, datetime
from django.utils import timezone
import pytz


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
            timezone.activate(pytz.timezone('US/Michigan'))
            now = timezone.now()
            tm = timezone.make_aware(datetime.strptime(tm, "%Y/%m/%d %H:%M"))
            try:
                if tm<=now:
                    err_msg="No past time!"
                elif 10<tm.hour<21:
                    object_list = Reserve.objects.filter(
                        Q(date__icontains=tm.strftime("%Y-%m-%d")) & Q(hour__icontains=tm.hour)
                    )
                    tb_dict = {}
                    for tb in Table.objects.all():
                        tb_dict[tb] = True
                    for res in object_list:
                        tb_dict[res.table] = False
                    tb_list += list(tb_dict.items())
                    '''
                    for tb, val in tb_dict.items():
                        tb_list.append((tb, val))
                    '''
                    tm_str = tm.strftime("%Y-%m-%d-%H")
                else:
                    err_msg="We open in 11:00~20:00"
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
        print("fv")
        object = form.save(commit=False)
        dh = datetime.strptime(self.request.GET.get('d'), "%Y-%m-%d-%H")
        object.custom = str(self.request.user)
        object.table = Table.objects.get(id=self.request.GET.get('n'))
        object.date = dh.strftime("%Y-%m-%d")
        object.hour = dh.hour
        '''
        if object.person>table.category.max_person:
            raise forms.ValidationError("Table %s con only contain %d diners"%(table, table.category.max_person))
        if object.person<table.category.min_person:
            raise forms.ValidationError("Table %s should have at least %d diners"%(table, table.category.min_person))
        '''
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

