from django.urls import path, include
from payapp.views.accountant_and_position import (index,
                                                  PositionDetailView,
                                                  accountant_creation,
                                                  accountant_update,
                                                  login_user,
                                                  accountant_details,
                                                  change_password, 
                                                  PositionCreateView,
                                                  PositionListView,
                                                  PositionUpdateView,
                                                  logout_view
                                                  )

from payapp.views.employee import (employee_creation, 
                                   view_employee, 
                                   employee_update,
                                   employee_details)
app_name="payapp"

urlpatterns = [
    # Home Page and others
    path('', index, name='index'),
    # Accountant Related
    path('accountant/create/',accountant_creation, name='accoutant_create'),
    path('accountant/update/self/',accountant_update, name='accountant_update'),
    path('accountant/details/', accountant_details, name='accountant_details'),
    # Position Related
    path('position/create/',PositionCreateView.as_view(), name='position_create'),
    path('position/',PositionListView.as_view(),name="position_list"),
    path('position/detail/<int:id>/', PositionDetailView.as_view(),  name="position_detail"),
    path('position/update/<int:id>/', PositionUpdateView.as_view(),name='position_update'),
    # Employee
    path('employee/create/', employee_creation, name='employee_create'),
    path('employee/',view_employee, name='employee_list'),
    path('employee/details/',employee_details, name='employee_details'),
    path('employee/update/self/',employee_update, name='employee_update'),
    # Authentication Related
    path('change-password/',change_password,name='change_password'),
    path('login/',login_user, name='login'),
    path('logout/',logout_view,name='logout'),
    # Payments related
]
