from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
#from .forms import RegisterForm

'''
# Create your views here.
def register(response):
    if response.method == "POST":
    form = RegisterForm(response.POST)
    if form.is_valid():
        form.save()

    return redirect("/home")
    else:
    form = RegisterForm()

    return render(response, "home/register.html", {"form":form})

# This is a little complex because we need to detect when we are
# running in various configurations
'''
class HomeView(View):
    def get(self, request) :
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        context = {
            'installed' : settings.INSTALLED_APPS,
            'islocal'   : islocal,
            'is_staff'  : (request.user.groups.filter(name="staff").count()>0)
        }
        return render(request, 'home/index.html', context)

