from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.models import User 


# Create your models here.
class Position(models.Model):
   id = models.BigAutoField(primary_key=True)
   name = models.CharField(max_length=400)

   def __str__(self):
       return self.name

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    position = models.ForeignKey(Position,on_delete=models.CASCADE,related_name='profile')
    
    def __str__(self):
       return self.user


class RoomType(models.Model):
   id = models.BigAutoField(primary_key=True)
   room_type = models.CharField(max_length=200,unique=True)
   price = models.IntegerField()
   max_people = models.IntegerField()
   updated_at = models.DateField(auto_now_add=True)
   created_at = models.DateField(auto_now=True)
   

   def __str__(self):
       return self.room_type
    
class Room(models.Model):
   id = models.BigAutoField(primary_key=True)
   room_name = models.CharField(max_length=200,unique=True)
   room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE,related_name='room')
   status = models.BooleanField()
   check_in_status = models.BooleanField()
   check_out_status = models.BooleanField()
   delete_status = models.BooleanField()
   updated_at = models.DateField(auto_now_add=True)
   created_at = models.DateField(auto_now=True)
   
   def __str__(self):
       return self.room_name
   
class IdCardType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=400,unique=True)
    
    def __str__(self):
        return self.name
    
    
class Customer(models.Model):
    ID_CARD_TYPE = {
        ('National Identity Card', 'National Identity Card'),
        ('Voter Id Card', 'Voter Id Card'),
        ('Pan Card', 'Pan Card'),
        ('Driving License', 'Driving License'),
    }
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=400)
    address = models.CharField(max_length=300)
    contact = models.CharField(max_length=300)
    email = models.CharField(max_length=200,null=False,blank=False)
    id_card_type = models.ForeignKey(IdCardType,on_delete=models.CASCADE, null=False, blank=False)
    id_card_no = models.CharField(max_length=20)
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='customer')
    check_in = models.DateField(null=True , blank=True)
    check_out = models.DateField(null=True , blank=True)
    is_check_out = models.BooleanField(default=False,null=True , blank=True)
    updated_at = models.DateField(auto_now_add=True)
    created_at = models.DateField(auto_now=True)
    
    def __str__(self):
       return self.name
    
class HotelReservation(models.Model):
   id = models.BigAutoField(primary_key=True)
   customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=False , blank=False)
   receptionist = models.CharField(max_length=200)
   room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='reservation')
   check_in = models.DateField(null=True , blank=True)
   check_out = models.DateField(null=True , blank=True)
   total = models.IntegerField(default=0,null=True , blank=True)
   remaining_price = models.IntegerField(default=0,null=True , blank=True)
   payment_status = models.BooleanField(default=False,null=True , blank=True)
   updated_at = models.DateField(auto_now_add=True)
   created_at = models.DateField(auto_now=True)
   
   def __int__(self):
       return self.customer

class Designation(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.name
    
class Shift(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.name
    

class Employee(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300,unique=True)
    designation = models.ForeignKey(Designation,on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    joining_date = models.CharField(max_length=300,null=True, blank=True)
    updated_at = models.DateField(auto_now_add=True)
    created_at = models.DateField(auto_now=True)
   
    def __str__(self):
       return self.name
   
class Complaint(models.Model):
    id = models.BigAutoField(primary_key=True)
    complaint_name = models.CharField(max_length=300)
    complaint_type = models.CharField(max_length=300)
    resolve = models.BooleanField(default=False,null=True, blank=True)
    budget = models.IntegerField(null=True, blank=True)
    updated_at = models.DateField(auto_now_add=True)
    created_at = models.DateField(auto_now=True)
   
    def __str__(self):
       return self.complaint_name

class HotelStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    name =models.CharField(max_length=400,)
    total_income= models.IntegerField(default=0,null=True,blank=True)
    pending_payment = models.IntegerField(default=0,null=True,blank=True)
    happy_customer = models.IntegerField(default = 0,null=True,blank=True)
    updated_at = models.DateField(auto_now_add=True)
    created_at = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Hotel Status'
   
    def __str__(self):
       return self.name

    
    


