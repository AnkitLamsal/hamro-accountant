from django.shortcuts import render
from ..forms import UserEmployeeForm
import stripe

def employee_creation(request): 
    if request.method == "POST":
        user_form = UserEmployeeForm(request.POST)
        if user_form.is_valid():
            user_form.save()
    elif request.method =="GET":
        user_form = UserEmployeeForm()
    context = {'user':user_form}
    return render(request, 'payapp/accountant_register.html',context)