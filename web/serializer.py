from rest_framework import serializers
from .models import *


      
class HotelReservationSerializers(serializers.ModelSerializer):
   class Meta:
      model = HotelReservation
      fields = '__all__'
      depth = 5
      
class CustomerSerializers(serializers.ModelSerializer):
   class Meta:
      model = Customer
      fields = '__all__'
      depth = 5
      
class RoomSerializers(serializers.ModelSerializer):
   reservation = HotelReservationSerializers(many=True, read_only=True).data
   customer = CustomerSerializers(many=True, read_only=True).data
   class Meta:
      model = Room 
      fields =('id','room_name','room_type','status','check_in_status','check_out_status','updated_at','created_at','reservation','customer')
      depth = 5
      
class RoomTypeSerializers(serializers.ModelSerializer):
   room = RoomSerializers(many=True, read_only=True).data
   class Meta:
      model = RoomType
      fields = ('id','room_type','price','max_people','updated_at','created_at',"room")
      depth = 5
      
      
class IdCardTypeSerializers(serializers.ModelSerializer):
   class Meta:
      model = IdCardType
      fields = '__all__'
      depth = 5
      
class EmployeeSerializers(serializers.ModelSerializer):
   class Meta:
      model = Employee
      fields = '__all__'
      depth = 5
      
class ShiftSerializers(serializers.ModelSerializer):
   class Meta:
      model = Shift
      fields = '__all__'
      depth = 5
      
class DepartmentSerializers(serializers.ModelSerializer):
   class Meta:
      model = Department
      fields = '__all__'
      depth = 5
      
      
class DesignationSerializers(serializers.ModelSerializer):
   class Meta:
      model = Designation
      fields = '__all__'
      depth = 5
      
      
class ComplaintSerializers(serializers.ModelSerializer):
   class Meta:
      model = Complaint
      fields = '__all__'
      depth = 5
      
class HotelStatusSerializers(serializers.ModelSerializer):
   class Meta:
      model = HotelStatus
      fields = '__all__'
      depth = 5
      
      
class ProfileSerializers(serializers.ModelSerializer): 
   class Meta:
      model = Profile
      fields = '__all__'
      depth = 5
      
      
class PositionSerializers(serializers.ModelSerializer):
   class Meta:
      model = Position
      fields = '__all__'
      depth = 5
      