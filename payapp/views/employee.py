from django.shortcuts import render, redirect
from ..forms import UserEmployeeForm, EmployeeForm
import stripe
stripe.api_key = "sk_test_51LFDP4IhxTYC5XjyJ4mJo4Zc48CSnR89ZPCb4RRqdBALg1cQQajUZWFV1m3GvxJlLQOvNQo3AYGOXyxO8F7UpPaY00Gdo1cwvA"


def employee_creation(request): 
    if request.method == "POST":
        user_form = UserEmployeeForm(request.POST)
        employee_form = EmployeeForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user_employee=employee_form.save(commit=False)
            user_employee.employee = user
            email = user.email
            print(email) 
            val = stripe.Account.create(type="standard", email=email)
            print(val['id'])
            user_employee.strip_account_id = val['id']
            user_employee.save()
            print(user_employee)
            print(user)
            return redirect('payapp:position_list')
    elif request.method =="GET":
        user_form = UserEmployeeForm()
        employee_form = EmployeeForm()
    context = {'user':user_form,'employee':employee_form}
    return render(request, 'payapp/employee_register.html',context)





# print(val['business_profile'])
