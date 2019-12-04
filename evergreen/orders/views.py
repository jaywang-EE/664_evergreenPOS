from django.views import View
from django.views import generic
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django import forms
from datetime import date, datetime

from .models import Meal, Order, MealNum
from reserve.models import Reserve

from home.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerDeleteView

from evergreen.timezone import ttos, stot


def itos2(price):
    return "%.2f"%price

def parse_order(odr):
    ml = MealNum.objects.filter(order=odr)
    return [odr, ml, itos2(sum(ml))]

def get_order_list(query_list):
    return [parse_order(odr) for odr in query_list]

class KitchenView(OwnerListView):
    def get(self, request):
        if request.user.groups.filter(name="staff").count()==0:
            raise Http404("No MyModel matches the given query.")
        order_list = Order.objects.filter(delivered=False)
        confirm_id = request.GET.get('c')
        #if confirm_id: confirm_id=int(confirm_id)
        print(confirm_id)
        if confirm_id: # set delivered
            order_list = order_list.exclude(id=confirm_id)
            odr = Order.objects.get(id=confirm_id)
            odr.delivered_at = datetime.now()
            odr.delivered = True
            odr.save()

        ctx = {'err_msg': "", 'order_list': get_order_list(order_list)}
        return render(request, 'kitchen_list.html', ctx)

class HistoryView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        ctx = {'err_msg': "", 'username':str(user), 
               'order_list': get_order_list(Order.objects.filter(owner=user)), 
               'reserve_list':Reserve.objects.filter(owner=user)}
        return render(request, 'hist_list.html', ctx)

class OrderListView(LoginRequiredMixin, View) :
    def get(self, request):
        ml = Meal.objects.all().order_by("name");
        meal_id = request.GET.get('m')
        num = request.GET.get('n')
        if num: num = int(num)
        is_delete = request.GET.get('d')
        err_msg = ""
        cookie_id = ""
        cart_list = []
        price = 0

        if (meal_id and num): 
            cookie_id = "meal_id_"+meal_id
            request.COOKIES[cookie_id] = num

        delete_list = []
        for k, v in request.COOKIES.items():
            if "meal_id_" in k:
                meal_id = k[8:]
                if is_delete in ["all", meal_id]:
                    delete_list.append(k)
                    continue
                meal = Meal.objects.get(id=meal_id)
                sub_price = meal.price*int(v)
                price += sub_price
                cart_list.append((meal.name, meal.image_url, meal.id, int(v), meal.price))

        if not cart_list: err_msg = "Please pick something into cart~"
        else: cart_list.sort()
        ctx = {'err_msg': err_msg, 'num_list': list(range(1,10)), 'meal_list':ml, 'cart_list': cart_list, 'price':itos2(price)}
        
        response = render(request, 'orders/order_list.html', ctx)
        # update cookie
        if is_delete:
            [response.delete_cookie(k) for k in delete_list]
        elif cookie_id: # update
            response.set_cookie(key=cookie_id, value=num)

        return response

class OrderCreateView(OwnerCreateView):
    model = Order
    fields = ['custom','phone','addr']
    template_name = "orders/order_form.html"

    def get_context_data(self, **kwargs):
        print(**kwargs)
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        cart_list = []
        price = 0.
        for k, v in self.request.COOKIES.items():
            if "meal_id_" in k:
                meal = Meal.objects.get(id=int(k[8:]));
                sub_price = meal.price*int(v)
                price += sub_price
                cart_list.append((meal.name, v, sub_price))
        context['cart_list'] = cart_list
        context['tot_price'] = itos2(price)
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

class OrderDeleteView(OwnerDeleteView):
    model = Order
    template_name = "orders/order_delete.html"

