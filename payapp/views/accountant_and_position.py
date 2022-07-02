from django.shortcuts import render
from django.http import HttpResponse
from ..forms import UserStaffForm, PositionForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from ..models import Accountant, Position
from django.views.generic import CreateView, ListView, DetailView, DeleteView,UpdateView
from django.urls import reverse,reverse_lazy
# Create your views here.

def index(request):
    return HttpResponse("Hello world");

def accountant_creation(request): 
    if request.method == "POST":
        user_form = UserStaffForm(request.POST)
        if user_form.is_valid():
            accountant = user_form.save()
            Accountant.objects.create(accountant = accountant)
            print("accountant created sucessfully.")
    elif request.method =="GET":
        user_form = UserStaffForm()
    context = {'user':user_form}
    return render(request, 'payapp/accountant_register.html',context)
        
def login_user(request):
    if request.method == "POST":
        form= AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print('valid form')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print("logged in")
    elif request.method == "GET":
            form = AuthenticationForm()
    context = {'user':form}
    return render(request, 'payapp/accountant_register.html',context)


class PositionCreateView(CreateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy('payapp:position_list')
    

class PositionListView(ListView):
    model = Position
    context_object_name = 'positions'
    
class PositionDetailView(DetailView):
    model = Position
    pk_url_kwarg= 'id'
    context_object_name='object'

class PositionUpdateView(UpdateView):
    model = Position
    form_class = PositionForm
    pk_url_kwarg= 'id'
    success_url = reverse_lazy('payapp:position_list')