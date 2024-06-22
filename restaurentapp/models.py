from django.db import models
from django.utils import timezone



# Create your models here.
class Category(models.Model):
   id = models.BigAutoField(primary_key=True)
   name = models.CharField(max_length=300)
   icon = models.TextField()
   
   class Meta:
      verbose_name = 'Category'
      verbose_name_plural = 'Categories'
      
   def __str__(self):
       return self.name

class MealItem(models.Model):
   id=  models.BigAutoField(primary_key=True)
   name = models.CharField(max_length=300)
   category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="mealitem")
   image = models.ImageField(upload_to='Meal')
   ingredients = models.TextField()
   price = models.IntegerField(default=0)
   updated_at = models.DateField(auto_now_add=True)
   created_at = models.DateField(auto_now=True)
   
   def __str__(self):
       return self.name   
    
class Floor(models.Model):
   id = models.BigAutoField(primary_key=True)
   name = models.CharField(max_length=300)
      
   def __str__(self):
       return self.name
    
class TableData(models.Model):
   id = models.BigAutoField(primary_key=True)
   name = models.CharField(max_length=300)
   floor = models.ForeignKey(Floor, on_delete=models.CASCADE,related_name="table")
   occupied = models.BooleanField()
      
   def __str__(self):
       return self.name

class Customer(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

   
class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    table = models.ForeignKey(TableData, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_choices = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')

    def __str__(self):
        return f'Order {self.id} by {self.customer.name}'

class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    meal = models.ForeignKey(MealItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_ready = models.BooleanField()

    def __str__(self):
        return f'{self.quantity} x {self.meal.name}'
    
    
class Notification(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return self.message
    
    
class BillReport(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_id = models.ForeignKey(OrderItem ,on_delete=models.CASCADE,null=True, blank=True)
    
    
class OrganizationDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=400,null=True, blank=True )
    address = models.CharField(max_length=400,null=True, blank=True )
    phone =models.CharField(max_length=20,null=True, blank=True )
    
    def __str__(self):
        return self.name
    
    
    
    
    