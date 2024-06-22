from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *
urlpatterns = [
   path('', login_view, name='login'),
   path('logout', logout_view, name='logout'),
   path('register', register_view, name='register'),
   path('room', login_required(roomScreen), name='room'),
   path('dashboard', login_required(dashboard_view), name='dashboard'),
   path('reservation',login_required(addReservation),name='reservation'),
   path('roomtype', login_required(roomtypeScreen), name='roomtype'),
   path('customer', login_required(customerScreen), name='customer'),
   path('staff', login_required(staff_view), name='staff'),
   path('complaint', login_required(complaint_view), name='complaint'),
   path('reservation/<int:room_id>/', reservation_details, name='reservation_details'),
   path('change_reservation/<int:room_id>/<int:customer_id>/<int:reservation_id>/', edit_reservation_view, name='edit_reservation_view'),
   path('complaint/<int:complaint_id>/', complaint_details, name='complaint_details'),
   path('staff/<int:employee_id>/', employee_details, name='employee_details'),
   path('room/<int:room_id>/', room_details, name='room_details'),
   path('roomtype/<int:roomtype_id>/', roomtype_details, name='roomtype_details'),
   path('delete_room/<int:id>/', delete_room, name='delete_room'),
   path('delete_roomtype/<int:id>/', delete_roomtype, name='delete_roomtype'),
   path('cancel_reservation/<int:id>/<int:customer_id>', cancel_reservation, name='cancel_reservation'),
   
   
   # for admin
   path('designation', login_required(designation_view), name='designation'),
   path('department', login_required(department_view), name='department'),
   path('id_card_type', login_required(id_card_type_view), name='id_card_type'),
   path('shift', login_required(shift_view), name='shift'),
   
   path('designation/<int:designation_id>', designation_details, name='designation_details'),
   path('department/<int:department_id>', department_details, name='department_details'),
   path('id_card_type/<int:id_card_type_id>', id_card_type_details, name='id_card_type_details'),
   path('shift/<int:shift_id>', shift_details, name='shift_detalis'),
   
   path('delete_designation/<int:designation_id>', delete_designation, name='delete_designation'),
   path('delete_department/<int:department_id>',delete_department, name='delete_department'),
   path('delete_id_card_type/<int:id_card_type_id>', delete_id_card_type, name='delete_id_card_type'),
   path('delete_shift/<int:shift_id>', delete_shift, name='delete_shift_detalis'),
]

