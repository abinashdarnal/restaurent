from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import *
from .serializer import *
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import login as auth_login  ,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User 
from datetime import datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
 
# Create your views here.

def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
 
        auth_user = authenticate(request, username=username, password=password)
        if auth_user is not None:
            auth_login(request, auth_user)
            return redirect('/dashboard')
        else:
            return JsonResponse({'message': 'Authentication failed'}, status=401)
           
    return render(request, 'login.html')

    

def register_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')

        if password!=confirm_password:
            return JsonResponse({"message":"Your password and confrom password are not Same!!"})
        else:
            user=User.objects.create_user(username,email,password)
            user.save()
            return redirect('/')

    return render (request,'register.html')
    
    
def logout_view(request):
    logout(request)
    return redirect('/')  
    
SideBar=[
    
    {"name" : "DashBoard " ,"link": "dashboard", "icons" : 'fa-solid fa-box',"admin":False },
    {"name" : "Manage Room " ,"link": "room", "icons" : 'fa-solid fa-box',"admin": False },
    {"name" : "Room Type" ,"link": "roomtype", "icons" : 'fa-solid fa-box' ,"admin":False},
    {"name" : "Guest" ,"link": "customer", "icons" : 'fa-solid fa-bag-shopping',"admin":False },
    {"name" : "Reservation " ,"link": "reservation", "icons" : 'fa-solid fa-box',"admin":False },
    {"name" : "Manage Statf " ,"link": "staff", "icons" : 'fa-solid fa-box',"admin":False },
    {"name" : "Complaints " ,"link": "complaint", "icons" : 'fa-solid fa-box',"admin":False },
    {"name" : "Designation " ,"link": "designation", "icons" : 'fa-solid fa-box' ,"admin":True},
    {"name" : "Department " ,"link": "department", "icons" : 'fa-solid fa-box',"admin":True },
    {"name" : "Id Card Type " ,"link": "id_card_type", "icons" : 'fa-solid fa-box',"admin":True },
    {"name" : "Shift " ,"link": "shift", "icons" : 'fa-solid fa-box',"admin":True },
    {"name" : "Restaurent" ,"link": "restaurent/table", "icons" : 'fa-solid fa-box',"admin":False },

]

def reservation_details(request, room_id):
    if request.method == "GET":
        reservation = get_object_or_404(HotelReservation, room__id=room_id)
        serializer = HotelReservationSerializers(reservation)
        return JsonResponse(serializer.data, safe=False)

def complaint_details(request, complaint_id):
    if request.method == "GET":
        complaint = get_object_or_404(Complaint, id=complaint_id)
        serializer = ComplaintSerializers(complaint)
        return JsonResponse(serializer.data, safe=False)
    
def employee_details(request, employee_id):
    if request.method == "GET":
        employee = get_object_or_404(Employee, id=employee_id)
        serializer = EmployeeSerializers(employee)
        return JsonResponse(serializer.data, safe=False)
    
def room_details(request, room_id):
    if request.method == "GET":
        room = get_object_or_404(Room, id=room_id)
        serializer = RoomSerializers(room)
        return JsonResponse(serializer.data, safe=False)

def delete_room(request, id):
    room = get_object_or_404(Room, id=id)
    room.delete()
    return redirect('/room')

def cancel_reservation(request, id,customer_id):
    room = get_object_or_404(Room, id=id)
    room.status = False
    room.check_in_status = False
    room.check_out_status = False
    room.save()
    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()
    
    return redirect('/room')
    
def roomtype_details(request, roomtype_id):
    if request.method == "GET":
        roomtype = get_object_or_404(RoomType, id=roomtype_id)
        serializer = RoomTypeSerializers(roomtype)
        return JsonResponse(serializer.data, safe=False)

def delete_roomtype(request, id):
    roomtype = get_object_or_404(RoomType, id=id)
    roomtype.delete()
    return redirect('/roomtype')

def designation_details(request,designation_id):
    designation =get_object_or_404(Designation,id=designation_id)
    serializer=DesignationSerializers(designation)
    return JsonResponse(serializer.data,safe=False )

def delete_designation(request,designation_id):
    designation =get_object_or_404(Designation,id=designation_id)
    designation.delete()
    return redirect('/designation')

def department_details(request,department_id):
    department =get_object_or_404(Department,id=department_id)
    serializer=DepartmentSerializers(department)
    return JsonResponse(serializer.data,safe=False )

def delete_department(request,department_id):
    department =get_object_or_404(Department,id=department_id)
    department.delete()
    return redirect('/department')

def shift_details(request,shift_id):
    shift =get_object_or_404(Shift,id=shift_id)
    serializer=ShiftSerializers(shift)
    return JsonResponse(serializer.data,safe=False )

def delete_shift(request,shift_id):
    shift =get_object_or_404(Shift,id=shift_id)
    shift.delete()
    return redirect('/shift')

def id_card_type_details(request,id_card_type_id):
    id_card_type =get_object_or_404(IdCardType,id=id_card_type_id)
    serializer=IdCardTypeSerializers(id_card_type)
    return JsonResponse(serializer.data,safe=False )

def delete_id_card_type(request,id_card_type_id):
    id_card_type =get_object_or_404(IdCardType,id=id_card_type_id)
    id_card_type.delete()
    return redirect('/id_card_type')

@login_required(login_url='/')
def roomScreen(request):
   
    if request.method == "POST":
        if 'search' in request.POST:
            search = request.POST.get("search", "")
            if search:
                context ={
                    "SideBar" : SideBar,
                    "Data" : RoomSerializers(Room.objects.filter(Q(room_name__contains=search) | Q(room_type_room_type__contains=search) | Q(price__contains=search)), many=True).data,
                    "Fields" : ["Room Name" ,"Room Type","Booking Status", "CheckIn Status", "CheckOut Status", "Activity"],
                    "Page" :"Room",
                    }
                return render(request, "room.html", context)
    if request.method == "POST":
        if 'room_name' in request.POST:
            room_name = request.POST.get('room_name')
            room_type = RoomType.objects.filter(room_type=request.POST.get('room_type')).first()
            status = False
            check_in_status = False
            check_out_status = False
            delete_status = False
            room = Room(
                room_name= room_name,
                room_type=room_type,
                status=status,
                check_in_status=check_in_status,
                check_out_status=check_out_status,
                delete_status=delete_status,
                )
            room.save()
            return redirect('/room')
    if request.method == "POST":
        if 'advance_payment' in request.POST:
                reservation_id = request.POST.get('reservation_id')
                room_id = request.POST.get('room_id')
                advance_payment = float(request.POST.get('advance_payment'))

                # Update the reservation with the advance payment
                reservation = get_object_or_404(HotelReservation, id=reservation_id)
                reservation.remaining_price = reservation.total - advance_payment 
                reservation.payment_status = True
                reservation.save()
                
                
                
                hotelStatus = HotelStatus.objects.first()
                hotelStatus.total_income = hotelStatus.total_income + advance_payment
                # Calculate the total remaining price for all reservations
                total_remaining_payment = HotelReservation.objects.aggregate(Sum('remaining_price'))['remaining_price__sum'] or 0
                hotelStatus.pending_payment = total_remaining_payment
                hotelStatus.save()

                room = get_object_or_404(Room, id = room_id)
                room.check_in_status = True
                room.delete_status = False
                room.save()

                # Return a response or render the updated context
                context = {
                    "SideBar": SideBar,
                    "Data": RoomSerializers(Room.objects.all(), many=True).data,
                    "RoomType": RoomTypeSerializers(RoomType.objects.all(), many=True).data,
                    "Reservation": HotelReservationSerializers(reservation, many=False).data,
                    "Fields": ["Room Name", "Room Type", "Booking Status", "CheckIn Status", "CheckOut Status", "Activity"],
                    "Page": "Room",
                }
                return redirect('/room')
    if request.method == "POST":
        if 'remaining_payment' in request.POST:
            reservation_id = request.POST.get('reservation_id')
            room_id = request.POST.get('room_id')
            customer_id = request.POST.get('customer_id')
            remaining_payment = float(request.POST.get('remaining_payment'))

            # Update the reservation with the advance payment
            reservation = get_object_or_404(HotelReservation, id=reservation_id)
            print(reservation)
            if reservation.remaining_price != remaining_payment:
                reservation.remaining_price -= remaining_payment
                if reservation.remaining_price <= 0:
                    reservation.payment_status = True  # Mark payment as complete if fully paid
                reservation.save()
                hotelStatus = HotelStatus.objects.first()
                hotelStatus.total_income = hotelStatus.total_income + remaining_payment
                hotelStatus.save()
            else:
                room = get_object_or_404(Room, id=room_id)
                room.check_out_status = True
                room.save()
                
                hotelStatus = HotelStatus.objects.first()
                hotelStatus.total_income = hotelStatus.total_income + remaining_payment
                hotelStatus.save()
                

                if room.check_out_status:
                    # Reset room status
                    room.status = False
                    room.check_in_status = False
                    room.check_out_status = False
                    room.save()
                    customer = get_object_or_404(Customer, id =customer_id)
                    customer.is_check_out = True
                    customer.save()
                    reservation.delete()
                    

                    return redirect('/room')

            # Update the reservation for partial payment
            

            # Return a response or render the updated context
            context = {
                "SideBar": SideBar,
                "Data": RoomSerializers(Room.objects.all(), many=True).data,
                "RoomType": RoomTypeSerializers(RoomType.objects.all(), many=True).data,
                "Reservation": HotelReservationSerializers(reservation, many=False).data,
                "Fields": ["Room Name", "Room Type", "Booking Status", "CheckIn Status", "CheckOut Status", "Activity"],
                "Page": "Room",
            }
            return redirect('/room')
    if request.method == "POST":
        if 'update_room_name' in request.POST:
            room_id = request.POST.get('room_id')
            room_name = request.POST.get('update_room_name')
            room_type = RoomType.objects.filter(room_type=request.POST.get('update_room_type')).first()
            room = get_object_or_404(Room, id=room_id)
            room.room_name = room_name
            room.room_type = room_type
            room.status = False
            room.check_in_status = False
            room.check_out_status = False
            room.delete_status = False
            room.save()
           
            return redirect('/room')
            
            
    context ={
        "SideBar" : SideBar,
        "Data" : RoomSerializers(Room.objects.all(), many=True).data,
        "RoomType":RoomTypeSerializers(RoomType.objects.all(), many=True).data,
        "Reservation": HotelReservationSerializers(HotelReservation.objects.first(),many=False).data,
        "Fields" : ["Room Name" ,"Room Type","Booking Status", "CheckIn Status", "CheckOut Status", "Activity"],
        "Page" :"Room",
        }
    return render(
        request,
        "room.html",
        context,
    ) 
 
@login_required(login_url='/')  
def roomtypeScreen(request):
    if request.method == "POST":
        if 'search' in request.POST:
            search = request.POST.get("search", "")
            if search:
                context ={
                    "SideBar" : SideBar,
                    "Data" : RoomTypeSerializers(RoomType.objects.filter(Q(room_type__contains=search) | Q(description__contains=search)), many=True).data,
                    "Fields" : ["SN","Room Type" ,"price",'Maximum People'],
                    "Page" :"Room Type",
                    }
                return render(request, "roomtype.html", context)
    if request.method == "POST":
        if 'room_type' in request.POST:
            room_type = request.POST.get('room_type')
            price = request.POST.get('price')
            max_people = request.POST.get('max_people')   
            roomtype = RoomType(room_type=room_type,max_people=max_people,price=price)
            roomtype.save()
            return redirect('/roomtype')
    if request.method == "POST":
        if 'update_room_type' in request.POST:
            roomtype_id = request.POST.get('roomtype_id')
            room_type = request.POST.get('update_room_type')
            price = request.POST.get('update_price')
            max_people = request.POST.get('update_max_people')
            
            roomtype = get_object_or_404(RoomType, id=roomtype_id)
            roomtype.room_type = room_type
            roomtype.price = price
            roomtype.max_people = max_people
            roomtype.save()
           
            return redirect('/roomtype')

    context ={
        "SideBar" : SideBar,
        "Data" : RoomTypeSerializers(RoomType.objects.order_by('-created_at'), many=True).data,
        "Fields" : ["SN","Room Type" ,"price",'Maximum People'],
        "Page" :"Room Type",
        }
    return render(
        request,
        "roomtype.html",
        context,
    ) 

@login_required(login_url='/')  
def customerScreen(request):
    if request.method == "POST":
        if 'search' in request.POST:
            search = request.POST.get("search", "")
            if search:
                context ={
                    "SideBar" : SideBar,
                    "Data" : CustomerSerializers(Customer.objects.filter(Q(name__contains=search) | Q(address__contains=search) | Q(contact__contains=search)| Q(gender__contains=search)), many=True).data,
                    "Fields" : ["SN","Name" ,"Address","Contact","Gender"],
                    "Page" :"Customer",
                    }
                return render(request, "customer.html", context)
    if request.method == "POST":
        if 'name' in request.POST:
            name = request.POST.get('name')
            address = request.POST.get('address')
            contact = request.POST.get('contact')
            gender = request.POST.get('gender')
            id_proof = request.FILES.get('id_proof')
            customer = Customer(name=name,address=address,contact=contact,gender=gender,id_proof=id_proof)
            customer.save()

    context ={
        "SideBar" : SideBar,
        "Data" : CustomerSerializers(Customer.objects.order_by('-created_at'), many=True).data,
        "Fields" : ["SN","Name" ,"Address","Contact","Alert Room", 'Activity'],
        "Page" :"Customer",
        }
    return render(
        request,
        "customer.html",
        context,
    ) 

@login_required(login_url='/')
def addReservation(request):
    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        receptionist = request.POST.get('receptionist')
        email = request.POST.get('email')
        id_card_type = IdCardType.objects.filter(name = request.POST.get('id_card_type')).first()
        id_card_no = request.POST.get('id_card_no')
        room_name = request.POST.get('room_name')
        room_type = request.POST.get('room_type')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        total = request.POST.get('total_cost')
        
        try:
            customer = Customer(
                name=name,
                address=address,
                contact=contact,
                email=email,
                id_card_type=id_card_type,
                id_card_no=id_card_no,
                room = Room.objects.filter(room_name = request.POST.get('room_name')).first(),
                check_in=check_in,
                check_out=check_out,
            )
            customer.save()

            room = get_object_or_404(Room, room_name=room_name)
            room.status = True
            room.delete_status = True
            room.save()

            HotelReservation(
                customer = Customer.objects.filter(name = name).first(),
                room = Room.objects.filter(room_name = room_name).first(),
                receptionist=receptionist,
                check_in=check_in,
                check_out=check_out,
                total = total,
            ).save()
            return redirect('/room')
        except Exception as e:
            return HttpResponse(f'All Fields Mandetory!')

    room_id = request.GET.get('room_id', '')
    room_name = request.GET.get('room_name', '')
    room_type = request.GET.get('room_type', '')
    
    

    context = {
        "SideBar": SideBar,
        "Data": HotelReservationSerializers(HotelReservation.objects.order_by('created_at'), many=True).data,
        "RoomType": RoomTypeSerializers(RoomType.objects.all(), many=True).data,
        "Room": RoomSerializers(Room.objects.all(), many=True).data,
        "IdCardType": IdCardTypeSerializers(IdCardType.objects.all(), many=True).data,
        "Fields": ["SN", "Customer", "Room", "Check In ", "Check Out"],
        "Page": "Reservation",
       
        "room_id": room_id,
        "room_name": room_name,
        "room_type": room_type,
       
    }
    return render(
        request,
        "addreservation.html",
        context,
    ) 
    
@login_required(login_url='/')
def edit_reservation_view(request,room_id, customer_id,reservation_id):
    room = get_object_or_404(Room, id=room_id)
    customer = get_object_or_404(Customer, id=customer_id)
    reservation = get_object_or_404(HotelReservation, id=reservation_id)
    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        receptionist = request.POST.get('receptionist')
        email = request.POST.get('email')
        id_card_type_name = request.POST.get('id_card_type')
        id_card_type = IdCardType.objects.filter(name=id_card_type_name).first()
        id_card_no = request.POST.get('id_card_no')
        room_name = request.POST.get('room_name')
        check_in_str = request.POST.get('check_in')
        check_out_str = request.POST.get('check_out')
        total = request.POST.get('total_cost')

        # Ensure the date strings are valid
        try:
            check_in = date.fromisoformat(check_in_str) if check_in_str else None
            check_out = date.fromisoformat(check_out_str) if check_out_str else None
        except ValueError:
            return HttpResponse("Invalid date format.", status=400)

        room.status = True
        room.delete_status = True
        room.save()

        customer.name = name
        customer.address = address
        customer.contact = contact
        customer.email = email
        customer.id_card_type = id_card_type
        customer.id_card_no = id_card_no
        customer.room = Room.objects.filter(room_name=room_name).first()
        customer.check_in = check_in
        customer.check_out = check_out
        customer.save()

        reservation.customer = customer
        reservation.room = customer.room
        reservation.receptionist = receptionist
        reservation.check_in = check_in
        reservation.check_out = check_out
        reservation.total = total
        reservation.save()

        return redirect('/room')


    context = {
        "SideBar": SideBar,
        "Data": HotelReservationSerializers(HotelReservation.objects.order_by('created_at'), many=True).data,
        "RoomType": RoomTypeSerializers(RoomType.objects.all(), many=True).data,
        "Room": RoomSerializers(Room.objects.all(), many=True).data,
        "IdCardType": IdCardTypeSerializers(IdCardType.objects.all(), many=True).data,
        "Fields": ["SN", "Customer", "Room", "Check In ", "Check Out"],
        "Page": "Reservation",
        "PlaceholderRoom": RoomSerializers(room).data,
        "PlaceholderCustomer": CustomerSerializers(customer).data,
        # "PlaceholderReservation": HotelReservation,
    }
    return render(
        request,
        "changereservation.html",
        context,
    ) 

@login_required(login_url='/')
def dashboard_view(request):  
    hotelStatus, created = HotelStatus.objects.get_or_create()

    total_remaining_payment = HotelReservation.objects.aggregate(Sum('remaining_price'))['remaining_price__sum'] or 0
    hotelStatus.pending_payment = total_remaining_payment
    hotelStatus.save()
    
    context ={
        "SideBar" : SideBar,
        "Data" : HotelReservationSerializers(HotelReservation.objects.order_by('created_at'), many=True).data,
        "Reserved":RoomSerializers(Room.objects.filter(Q(status=True)), many=True ).data,
        "Available":RoomSerializers(Room.objects.filter(Q(status=False)), many=True ).data,
        "Booked":RoomSerializers(Room.objects.filter(Q(check_in_status=True)), many=True ).data,
        "Room":RoomSerializers(Room.objects.all(), many=True ).data,
        "Staff":EmployeeSerializers(Employee.objects.all(), many=True ).data,
        "Complaint":ComplaintSerializers(Complaint.objects.all(), many=True ).data,
        "PendingComplaint":ComplaintSerializers(Complaint.objects.filter(Q(resolve=False)), many=True ).data,
        "Customer":CustomerSerializers(Customer.objects.all(), many=True ).data,
        "HotelStatus":HotelStatusSerializers(HotelStatus.objects.first(), many=False ).data,
        "Page" :"DashBoard",
    }
    return render(
        request,
        'dashboard.html',
        context,
    )
    
@login_required(login_url='/')
def staff_view(request):
    if request.method == "POST":
        if 'search' in request.POST:
            search = request.POST.get("search", "")
            if search:
                context ={
                    "SideBar" : SideBar,
                    "Data" : EmployeeSerializers(Employee.objects.filter(Q(name__contains=search)  ), many=True).data,
                    "Fields" : ["SN","Name" ,"Designation","Department","Salary","Shift","Joining Date","Change Shift"],
                    "Page" :"Reservation",
                    }
                return render(request, "reservation.html", context)
    if request.method == "POST":
        if 'staff_name' in request.POST:
            name = request.POST.get('staff_name')
            designation = Designation.objects.filter(name = request.POST.get('designation')).first()
            department = Department.objects.filter(name = request.POST.get('department')).first()
            salary = request.POST.get('salary')
            shift = Shift.objects.filter(name = request.POST.get('shift')).first()
            joining_date = request.POST.get('joining_date')
            
            employee = Employee(
                name=name,
                designation=designation,
                department=department,
                salary=salary,
                shift=shift,
                joining_date=joining_date,
            )
            employee.save()
            return redirect('/staff')
    if request.method == "POST":
        if 'changed_shift' in request.POST:
            employee_id = request.POST.get('employee_id')
            shift = Shift.objects.filter(name = request.POST.get('changed_shift')).first()
            employee = get_object_or_404(Employee, id=employee_id)
            employee.shift = shift
            employee.save()
            return redirect('/staff')
            
    context ={
        "SideBar" : SideBar,
        "Data" : EmployeeSerializers(Employee.objects.all(), many=True).data,
        "Shift" : ShiftSerializers(Shift.objects.all(), many=True).data,
        "Department" : DepartmentSerializers(Department.objects.all(), many=True).data,
        "Designation" : DesignationSerializers(Designation.objects.all(), many=True).data,
        "Fields" : ["SN","Name" ,"Designation","Department","Salary","Shift","Joining Date","Change Shift"],
        "Page" :"Staff",
    }
    return render(
        request,
        'staff.html',
        context,
    )
    
@login_required(login_url='/')
def complaint_view(request):
    if request.method == "POST":
        if 'search' in request.POST:
            search = request.POST.get("search", "")
            if search:
                context ={
                    "SideBar" : SideBar,
                    "Data" : ComplaintSerializers(Complaint.objects.filter(Q(complaint_name__contains=search)  ), many=True).data,
                    "Fields" : ["SN","complaint name" ,"complaint type","complaint incounter","resolve","budget"],
                    "Page" :"Complaint",
                    }
                return render(request, 'complaint.html', context)
    if request.method == "POST":
        if 'complaint_name' in request.POST:
            complaint_name = request.POST.get('complaint_name')   
            complaint_type = request.POST.get('complaint_type')
            
            complaint = Complaint(complaint_type=complaint_type,complaint_name=complaint_name)
            complaint.save()
            return redirect('/complaint')
    if request.method == "POST":
        if 'budget' in request.POST:
            complaint_id = request.POST.get('complaint_id')
            budget = float(request.POST.get('budget'))
            
            complaint= get_object_or_404(Complaint, id=complaint_id)
            complaint.budget = budget
            complaint.resolve =True
            complaint.save()
            
            hotelStatus = HotelStatus.objects.first()
            hotelStatus.total_income = hotelStatus.total_income - budget
            hotelStatus.save()
                
            context = {
               "SideBar" : SideBar,
                "Data" : ComplaintSerializers(Complaint.objects.all(), many=True).data,
                "Reserved":RoomSerializers(Room.objects.filter(Q(status=True)), many=True ).data,
                "Available":RoomSerializers(Room.objects.filter(Q(status=False)), many=True ).data,
                "Room":RoomSerializers(Room.objects.all(), many=True ).data,
                "IdCardType":IdCardTypeSerializers(IdCardType.objects.all(), many=True ).data,
                "Fields" : ["SN","complaint name" ,"complaint type","complaint incounter","resolve","budget"],
                "Page" :"Complaint",
            }
            return redirect('/complaint')
    context ={
        "SideBar" : SideBar,
        "Data" : ComplaintSerializers(Complaint.objects.all(), many=True).data,
        "Reserved":RoomSerializers(Room.objects.filter(Q(status=True)), many=True ).data,
        "Available":RoomSerializers(Room.objects.filter(Q(status=False)), many=True ).data,
        "Room":RoomSerializers(Room.objects.all(), many=True ).data,
        "IdCardType":IdCardTypeSerializers(IdCardType.objects.all(), many=True ).data,
        "Fields" : ["SN","complaint name" ,"complaint type","complaint incounter","resolve","budget"],
        "Page" :"Complaint",
    }
    return render(
        request,
        'complaint.html',
        context,
    )
    
@login_required(login_url='/')
@staff_required(login_url='/')
def designation_view(request):
    if request.method == "POST":
        if 'search' in request.POST:
            search = request.POST.get("search", "")
            if search:
                context ={
                    "SideBar" : SideBar,
                    "Data" : DesignationSerializers(Designation.objects.filter(Q(name__contains=search)), many=True).data,
                    "Fields" : ["SN","Name"],
                    "Page" :"Designation",
                    }
                return render(request,  "designation.html", context)
    if request.method == "POST":
        if 'name' in request.POST:
            name = request.POST.get('name')   
            
            designation = Designation(name=name)
            designation.save()
            return redirect('/designation')
    if request.method == "POST":
        if 'update_name' in request.POST:
            designation_id = request.POST.get('designation_id')
            update_name = request.POST.get('update_name')   
            
            designation = get_object_or_404(Designation, id=designation_id)
            designation.name = update_name
            designation.save()
            return redirect('/designation')
    context ={
        "SideBar" : SideBar,
        "Data" : DesignationSerializers(Designation.objects.all(), many=True).data,
        "Fields" : ["SN","Name"],
        "Page" :"Designation",
    }
    return render(
        request,
        "designation.html",
        context,
    )    
    
    
@login_required(login_url='/')
@staff_required(login_url='/')
def department_view(request):
    if request.method == "POST":
        if 'search' in request.POST:
            search = request.POST.get("search", "")
            if search:
                context ={
                    "SideBar" : SideBar,
                    "Data" : DepartmentSerializers(Department.objects.filter(Q(name__contains=search)), many=True).data,
                    "Fields" : ["SN","Name"],
                    "Page" :"Department",
                    }
                return render(request,  "department.html", context)
    if request.method == "POST":
        if 'name' in request.POST:
            name = request.POST.get('name')   
            
            department = Department(name=name)
            department.save()
            return redirect('/department')
    if request.method == "POST":
        if 'update_name' in request.POST:
            department_id = request.POST.get('department_id')
            update_name = request.POST.get('update_name')   
            
            department = get_object_or_404(Department, id=department_id)
            department.name = update_name
            department.save()
            return redirect('/department')
    context ={
        "SideBar" : SideBar,
        "Data" : DepartmentSerializers(Department.objects.all(), many=True).data,
        "Fields" : ["SN","Name"],
        "Page" :"Department",
    }
    return render(
        request,
        "department.html",
        context,
    )    
    
    
@login_required(login_url='/')
@staff_required(login_url='/')
def id_card_type_view(request):
    if request.method == "POST":
        if 'search' in request.POST:
            search = request.POST.get("search", "")
            if search:
                context ={
                    "SideBar" : SideBar,
                    "Data" : IdCardTypeSerializers(IdCardType.objects.filter(Q(name__contains=search)), many=True).data,
                    "Fields" : ["SN","Name"],
                    "Page" :"IdCardType",
                    }
                return render(request,  "id_card_type.html", context)
    if request.method == "POST":
        if 'name' in request.POST:
            name = request.POST.get('name')   
            
            id_card_type = IdCardType(name=name)
            id_card_type.save()
            return redirect('/id_card_type')
    if request.method == "POST":
        if 'update_name' in request.POST:
            idcard_id = request.POST.get('idcard_id')
            update_name = request.POST.get('update_name')   
            
            id_card_type = get_object_or_404(IdCardType, id=idcard_id)
            id_card_type.name = update_name
            id_card_type.save()
            return redirect('/id_card_type')
    context ={
        "SideBar" : SideBar,
        "Data" : IdCardTypeSerializers(IdCardType.objects.all(), many=True).data,
        "Fields" : ["SN","Name"],
        "Page" :"IdCardType",
    }
    return render(
        request,
        "idCardtype.html",
        context,
    )    
    
    
@login_required(login_url='/')
@staff_required(login_url='/')
def shift_view(request):
    if request.method == "POST":
        if 'search' in request.POST:
            search = request.POST.get("search", "")
            if search:
                context ={
                    "SideBar" : SideBar,
                    "Data" : ShiftSerializers(Shift.objects.filter(Q(name__contains=search)), many=True).data,
                    "Fields" : ["SN","Name"],
                    "Page" :"Shift",
                    }
                return render(request,  "shift.html", context)
    if request.method == "POST":
        if 'name' in request.POST:
            name = request.POST.get('name')   
            
            shift = Shift(name=name)
            shift.save()
            return redirect('/shift')
    if request.method == "POST":
        if 'update_name' in request.POST:
            shift_id = request.POST.get('shift_id')
            update_name = request.POST.get('update_name')   
            
            shift = get_object_or_404(Shift, id=shift_id)
            shift.name = update_name
            shift.save()
            return redirect('/shift')
    context ={
        "SideBar" : SideBar,
        "Data" : ShiftSerializers(Shift.objects.all(), many=True).data,
        "Fields" : ["SN","Name"],
        "Page" :"Shift",
    }
    return render(
        request,
        "shift.html",
        context,
    )    
