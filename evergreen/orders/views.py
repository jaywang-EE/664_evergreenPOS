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

from .models import Meal, Order, MealNum
from reserve.models import Reserve

from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

class KitchenView(OwnerListView):
    def get(self, request):
        if not request.user.is_superuser():
            raise Http404("No MyModel matches the given query.")
        order_list = []
        for odr in Order.objects.all(): pass


class HistoryView(LoginRequiredMixin, View) :
    def get(self, request):
        order_list = []
        timezone.activate(pytz.timezone('US/Michigan'))
        for order in Order.objects.filter(owner=self.request.user):
            price = 0
            order_list.append([timezone.localtime(order.created_at).strftime("%Y-%m-%d %H:%M"), []])
            for mn in MealNum.objects.filter(order=order):
                price += mn.meal.price*mn.num
                order_list[-1][1].append((mn.meal.name, mn.num))
            order_list[-1].append(price)

        reserve_list = []
        for res in Reserve.objects.filter(owner=self.request.user):
            reserve_list.append((str(res.date), res.hour, str(res.table)))

        ctx = {'err_msg': "", 'order_list': order_list, 'reserve_list':reserve_list, 'username':str(self.request.user)}
        return render(request, 'orders/hist_list.html', ctx)


class OrderListView(LoginRequiredMixin, View) :
    def get(self, request):
        ml = Meal.objects.all();
        meal_id = request.GET.get('m')
        num = request.GET.get('n')
        if num: num = int(num)
        is_delete = request.GET.get('d')
        err_msg = ""
        cookie_id = ""
        cart_list = []
        price = 0

        if (meal_id and num):
            meal = Meal.objects.get(id=meal_id)
            meal_id = meal.id
            cookie_id = "meal_id_%d"%meal_id
            sub_price = meal.price*num
            price += sub_price
            cart_list = [(meal.name, meal.id, int(num), sub_price),]

        delete_all_list = []
        for k, v in request.COOKIES.items():
            if "meal_id_" in k:
                if is_delete == "all": 
                    delete_all_list.append(k)
                    continue
                if meal_id==int(k[8:]): continue
                if k[8:]==is_delete: continue
                meal = Meal.objects.get(id=int(k[8:]))
                sub_price = meal.price*int(v)
                price += sub_price
                cart_list.append((meal.name, meal.id, int(v), sub_price))

        if not cart_list: err_msg = "Put something into Cart!"

        ctx = {'err_msg': err_msg, 'num_list': list(range(1,10)), 'meal_list':ml, 'cart_list': cart_list, 'price':"%.2f"%price}
        response = render(request, 'orders/order_list.html', ctx)
        if is_delete=="all":
            [response.delete_cookie(k) for k in delete_all_list]
        elif is_delete:
            print("del: ",is_delete)
            response.delete_cookie('meal_id_%d'%int(is_delete))
        elif cookie_id:
            print("set: ",cookie_id)
            response.set_cookie(key=cookie_id, value=num)
        return response

class OrderDetailView(OwnerDetailView):
    model = Order
    template_name = "orders/order_detail.html"

class OrderCreateView(OwnerCreateView):
    model = Order
    form_class = CreateForm
    template_name = "orders/order_form.html"

    def get_context_data(self, **kwargs):
        print(**kwargs)
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        cart_list = []
        for k, v in self.request.COOKIES.items():
            if "meal_id_" in k:
                cart_list.append((Meal.objects.get(id=int(k[8:])).name,v))
        context['cart_list'] = cart_list
        return context

    def form_valid(self, form):
        response = super(OrderCreateView, self).form_valid(form)#form.save(commit=False)
        for k, v in self.request.COOKIES.items():
            if "meal_id_" in k:
                print("add meal", k)
                meal = Meal.objects.get(id=int(k[8:]))
                obj = MealNum.objects.create(order=self.object, meal=meal, num=v)
                obj.save()
                print("delete: ",k)
                response.delete_cookie(k)
        return response

    def get_initial(self):
        initial = super(OrderCreateView, self).get_initial()
        initial['custom'] = str(self.request.user)
        return initial

class OrderUpdateView(OwnerUpdateView):
    model = Order
    fields = ['custom', 'date', 'hour']
    template_name = "orders/order_form.html"

class OrderDeleteView(OwnerDeleteView):
    model = Order
    template_name = "orders/order_delete.html"

