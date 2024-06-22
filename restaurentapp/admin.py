from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
   list_display = ('id','name')
   list_display_links = ('id','name')
   
@admin.register(MealItem)
class MealItemAdmin(admin.ModelAdmin):
   list_display = ('name','category','price')
   list_display_links = ('name','category','price')
   
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
   list_display = ('customer','table')
   list_display_links = ('customer','table')
   
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
   list_display = ('name','phone')
   list_display_links = ('name','phone')
   
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
   list_display = ('order','meal','quantity','price')
   list_display_links = ('order','meal','quantity','price')
   
@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
   list_display = ('id',"name")
   list_display_links = ('id',"name")
   
@admin.register(TableData)
class TableDataAdmin(admin.ModelAdmin):
   list_display = ('id',"name")
   list_display_links = ('id',"name")
   
   
@admin.register(OrganizationDetail)
class OrganizationDetailAdmin(admin.ModelAdmin):
   list_display = ('id',"name","address","phone")
   list_display_links = ('id',"name","address","phone")
   
@admin.register(BillReport)
class BillReportAdmin(admin.ModelAdmin):
   list_display = ('id',"customer","phone","table","total_bill")
   list_display_links = ('id',"customer","phone","table","total_bill")