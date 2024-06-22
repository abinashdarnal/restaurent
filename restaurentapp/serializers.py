from rest_framework import serializers
from .models import *


class MealItemSerializers(serializers.ModelSerializer):
   class Meta:
      model = MealItem
      fields = "__all__"
      depth = 10


class CategorySerializers(serializers.ModelSerializer):
   mealitem = MealItemSerializers(many=True, read_only=True).data
   class Meta:
      model = Category
      fields = ('id','name','icon','mealitem')
      depth = 10

class TableDataSerializers(serializers.ModelSerializer):
   class Meta:
      model = TableData
      fields = "__all__"
      depth = 10
      
class FloorSerializers(serializers.ModelSerializer):
   table = TableDataSerializers(many=True, read_only=True).data
   class Meta:
      model = Floor
      fields = ('id','name','table')
      depth =10
      
class CustomerSerializers(serializers.ModelSerializer):
   class Meta:
      model = Customer
      fields = "__all__"
      depth = 10
      
class OrderItemSerializers(serializers.ModelSerializer):
   class Meta:
      model = OrderItem
      fields = "__all__"
      depth = 10
      
class OrganizationDetailSerializers(serializers.ModelSerializer):
   class Meta:
      model = OrganizationDetail
      fields = "__all__"
      depth = 10
      
class BillReportSerializers(serializers.ModelSerializer):
   class Meta:
      model = BillReport
      fields = "__all__"
      depth = 10
      
class OrderSerializers(serializers.ModelSerializer):
   order_items = OrderItemSerializers(many=True, read_only=True).data
   class Meta:
      model = Order
      fields = ('id','created_at','updated_at','status','customer','table','order_items')
      depth = 10