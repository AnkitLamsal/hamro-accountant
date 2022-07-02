from django.urls import path, include
from payapp.views.accountant_and_position import (PositionDetailView, 
                    index, 
                    accountant_creation, 
                    login_user, 
                    PositionCreateView,
                    PositionListView,
                    PositionUpdateView,
                    logout_view
                    )

from payapp.views.employee import employee_creation, view_employee
app_name="payapp"

urlpatterns = [
    path('', index, name='index'),
    path('accountant/create/',accountant_creation, name='accoutant_create'),
    path('login/',login_user, name='login'),
    path('logout/',logout_view,name='logout'),
    path('position/create/',PositionCreateView.as_view(), name='position_create'),
    path('position/',PositionListView.as_view(),name="position_list"),
    path('position/detail/<int:id>/', PositionDetailView.as_view(),  name="position_detail"),
    path('position/update/<int:id>/', PositionUpdateView.as_view(),name='position_update'),
    path('employee/create/', employee_creation, name='employee_create'),
    path('employee/',view_employee, name='employee_list'),
]
