from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import * 



urlpatterns = [
   # path('', login_view, name='login'),
   # path('logout', logout_view, name='logout'),
   # path('register', register_view, name='register'),
   path('menu/<int:table_id>/<str:customer_name>', login_required(menu_by_view), name='menu_cat'),   
   path('menu/<int:table_id>/<str:customer_name>/<str:catName>', login_required(menu_by_view), name='menu_cat'),   
   path('table', login_required(table_view), name='table'),   
   path('kot', login_required(kot_view), name='kot'),   
   path('addtable', login_required(add_table_view), name='add_table_view'),   
   path('addfloor', login_required(add_floor_view), name='add_floor_view'),   
   path('addcategory', login_required(add_category_view), name='add_category_view'),   
   path('addmeal', login_required(add_meal_view), name='add_meal_view'),   
   path('table/<int:table_id>', table_details, name='table_details'),
   path('viewtable/<int:table_id>', view_table_details, name='view_table_details'),
   path('delete_table/<int:table_id>', delete_table, name='delete_table'),
   path('cancel_order/<int:order_id>/<int:table_id>/<str:customer_name>', cancel_order, name='cancel_order'),
   path('cancel_order/<int:order_id>/<int:table_id>/<str:customer_name>/<str:catName>', cancel_order, name='cancel_order'),
   # path('/restaurent/meal/<int:mealId>', insert_meal, name='insert_meal'),
   path('delete_category/<int:cat_id>', delete_category, name='delete_category'),
   path('delete_floor/<int:floor_id>', delete_floor, name='delete_floor'),
   path('delete_table/<int:table_id>', delete_table, name='delete_table'),
   path('delete_meal/<int:meal_id>', delete_meal, name='delete_meal'),
   
   # path('orders/<int:order_id>', generate_pdf, name='generate_pdf'),
   path('orders/<int:order_id>', GenerateBillView.as_view(), name='generate_bill'),
   path('delete_order_after_payment/<int:order_id>', delete_order_after_payment, name='delete_order_after_payment'),

   path('order_ready/<int:order_id>', order_ready, name='order_ready'),

   #  path('generate_pdf/<int:id>/', generate_pdf, name='generate_pdf'),
   
   
]