from django.shortcuts import render, redirect
from django.urls import reverse,reverse_lazy
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from ..forms import PaymentForm, UserEmployeeForm, EmployeeForm, UserEditForm
import stripe
from ..models import Employee, Payment
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.models import User
import datetime
from django.views.generic import CreateView


stripe.api_key = "sk_test_51LFDP4IhxTYC5XjyJ4mJo4Zc48CSnR89ZPCb4RRqdBALg1cQQajUZWFV1m3GvxJlLQOvNQo3AYGOXyxO8F7UpPaY00Gdo1cwvA"


@login_required(login_url=reverse_lazy('payapp:login'))
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


@login_required(login_url=reverse_lazy('payapp:login'))
def view_employee(request):
    context = {}
    employees = Employee.objects.all()
    context['employees']= employees
    return render(request,'payapp/employee_list.html',context)


def employee_update(request):
    context = {}
    user = request.user
    if request.method == "GET":
        form = UserEditForm(instance=user)
        employee = user.employee
        user_form = EmployeeForm(instance = employee)
        context['form'] = form
        context['employee_form'] = user_form
    elif request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        employee = user.employee        
        user_form = EmployeeForm(request.POST,instance =  employee)
        if form.is_valid() and user_form.is_valid():
            # print(form.cleaned_data)
            form.save()
            user_form.save()
            return redirect('payapp:index')
        context['form'] = form
        context['employee_form'] = user_form
    return render(request,'payapp/employee_update.html',context)

def employee_details(request):
    return render(request,'payapp/employee_details.html')

class PayementCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payapp/payment_create.html'
    success_url = reverse_lazy('payapp:index')

    def get_form(self, form_class=None):
        """Returns an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(accountant = self.request.user.accountant,**self.get_form_kwargs())
    
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form.cleaned_data)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        accountant = self.request.user.accountant
        (tax_amount,
        pf_amount,
        user_salary,
        employee,
        pf_percent,
        payment_month) = self.deduct_amount(form)
        today = datetime.date.today()            
        val = stripe.Transfer.create(amount=int(user_salary),
                             currency="usd",
                             destination=employee.strip_account_id,
                                ) 
        pay = self.model.objects.create(
                tax_amount = tax_amount,
                pf_amount = pf_amount,
                payment_pf_percent = pf_percent,
                user_salary=user_salary,
                accountant = accountant,
                employee=employee,
                payment_date=today,
                payment_month = payment_month   
            )
        return HttpResponseRedirect(reverse_lazy('payapp:index'))
        
    def deduct_amount(self,form):
        '''Custom Function for deducting tax, provident fund and misc tax.'''
        employee = form['employee']
        total_salary = form['total_salary']
        payment_month = form['payment_month']
        pf_percent = employee.pf_percent
        print(pf_percent)
        print(f'Total Salary: {total_salary}')
        pf_amount = ((pf_percent)/100)*(total_salary)
        print(f'Provident Fund Amount:{pf_amount}')
        deducted_salary = total_salary - pf_amount
        print(f'Deducted Salary:{deducted_salary}')
        tax_amount = (1/100)*(deducted_salary)
        print(f'Tax amount: {tax_amount}')
        print(employee)
        user_salary = deducted_salary - tax_amount
        return tax_amount,pf_amount,user_salary,employee,pf_percent,payment_month 


# def payment_create(request):
#     context = {}
#     payment = PaymentForm(accountant=request.user.accountant)
#     if request.method == "POST": 
#         payment = PaymentForm(request.user.accountant,request.POST)
#         print(payment.is_valid())
#         if(payment.is_valid()):
#             accountant = request.user.accountant
#             (tax_amount,
#              pf_amount,
#              user_salary,
#              employee,
#              pf_percent,
#              payment_month) = deduct_amount(payment.cleaned_data)
#             today = datetime.date.today()            
#             val = stripe.Transfer.create(amount=int(user_salary),
#                              currency="usd",
#                              destination=employee.strip_account_id,
#                                 ) 
#             pay = Payment.objects.create(
#                 tax_amount = tax_amount,
#                 pf_amount = pf_amount,
#                 payment_pf_percent = pf_percent,
#                 user_salary=user_salary,
#                 accountant = accountant,
#                 employee=employee,
#                 payment_date=today,
#                 payment_month = payment_month   
#             )
#             print(pay)
#             return redirect('payapp:index')
#     elif request.method == "GET":
#         context['form'] = payment
#     return render(request,'payapp/payment_create.html',context)







class PaymentListView(ListView):
    model = Payment
    context_object_name = 'payments'
    
class UserListView(ListView):
    template_name = "payapp/user_list.html"
    model = User
    context_object_name = 'users'
    
    
def show_employee_balance(request,id):
    payments = Payment.objects.filter(employee = id)
    context = {}
    total_salary = 0.0
    total_provident_fund = 0.0
    total_tax = 0.0
    for payment in payments:
        total_salary += payment.user_salary
        total_provident_fund += payment.pf_amount
        total_tax += payment.tax_amount
    context['total_salary'] = total_salary
    context['total_provident_fund'] = total_provident_fund
    context['total_tax'] = total_tax
    return render(request, 'payapp/balance_view.html',context)


def view_transaction_details(request,id):
    context = {}
    transaction = Payment.objects.filter(employee = id)
    context['transactions'] = transaction
    return render(request,'payapp/salary_list.html',context)



def show_beruju(request,id):
    if request.method == "GET":
        print(request)
        months = []
        total_salaries = []
        for payment in  Payment.objects.filter(employee=id):
            pf_deducted = payment.user_salary + payment.tax_amount
            total_salary = pf_deducted + payment.pf_amount
            total_salaries.append(total_salary)
            month = payment.payment_month
            months.append(month)
        total_month = sum(months)
        net_salary = sum(total_salaries)
        x = Employee.objects.get(id = id)
        print(x.employee)
        base_salary = x.position.base_salary
        print(net_salary,total_month)
        print(base_salary)
        context = {}
        if(base_salary*total_month < net_salary):
            context['beruju'] = "yes"
            context['beruju_amount'] = net_salary - base_salary*total_month
        elif (base_salary*total_month == net_salary):
            context['beruju'] = 'equal'
        else:
            context['beruju'] = 'no'
        return JsonResponse(context, status = 200)
    return redirect('payapp:employee_list')