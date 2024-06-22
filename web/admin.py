from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
   list_display = ('id','name')
   list_display_links = ('id','name')
   
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
   list_display = ('user','position')
   list_display_links = ('user','position')
    
@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
   list_display = ('room_type','price','max_people','updated_at', 'created_at')
   search_fields = ('room_type','price','max_people')
   
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
   list_display = ('room_name','room_type','updated_at', 'created_at')
   search_fields = ('room_name','room_type')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
   list_display = ('name', 'address', 'contact', 'email', 'updated_at', 'created_at')
   search_fields=('name', 'address','contact','gender')
   
@admin.register(HotelReservation)
class HotelReservationAdmin(admin.ModelAdmin):
   list_display = (  'check_in', 'check_out', 'updated_at', 'created_at')
   

@admin.register(IdCardType)
class IdCardTypeAdmin(admin.ModelAdmin):
   list_display = ('id', 'name')
   search_fields=('id', 'name')
   
@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
   list_display = ('id','name')
   list_display_links = ('id','name')
   
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
   list_display = ('id','name')
   list_display_links = ('id','name')
   
@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
   list_display = ('id','name')
   list_display_links = ('id','name')
   
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
   list_display = ('name','designation','department','salary','shift','joining_date')
   search_fields = ('name','designation','department','salary','shift','joining_date')
   
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
   list_display = ('complaint_name','complaint_type','resolve','budget')
   search_fields = ('complaint_name','complaint_type','resolve','budget')

@admin.register(HotelStatus)
class HotelStatusAdmin(admin.ModelAdmin):
   list_display = ('name','total_income','pending_payment','happy_customer')
   
   
   
   
   