from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserStaffForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .models import Accountant
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


# def login_user(request):        
#     if request.method == "POST":
#         form = AuthenticationForm(request.POST)
#         print('form')
#         if form.is_valid():
#             print('valid form')
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']       
#             user = authenticate(username=username, password=password)
#             if user is None:
#                 print('jel')
#     elif request.method == "GET":
#         form = AuthenticationForm()
#     context = {'user':form}
#     return render(request, 'payapp/accountant_register.html',context)
        
        
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
# 				messages.info(request, f"You are now logged in as {username}.")
# 				return redirect("main:homepage")
# 			else:
# 				messages.error(request,"Invalid username or password.")
# 		else:
# 			messages.error(request,"Invalid username or password.")
# 	form = AuthenticationForm()
# 	return render(request=request, template_name="main/login.html", context={"login_form":form})
    
    
