from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login as auth_login  ,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.models import User 
from .models import *
from .serializers import *
from collections import defaultdict
from django.utils.deprecation import MiddlewareMixin
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.db.models import Sum
from io import BytesIO



# Create your views here.
def delete_order_after_payment(request, order_id):
    order = get_object_or_404(OrderItem, order__id = order_id)
    print(order.order.customer.name)
    print(order.order.customer.phone)
    print(order.price)
    print(order.order.table.name)
    print(order.order.updated_at)
    
    table = get_object_or_404(TableData, id = order.order.table.id)
    table.occupied = False
    table.save()
     
    save_order = BillReport(
        customer = order.order.customer.name,
        phone = order.order.customer.phone,
        total_bill = order.price,
        table = order.order.table.name,
        order_date = order.order.updated_at, 
    )
    
    save_order.save()
    order.delete()
    
    return redirect("/restaurent/table")


    

def generate_pdf(html_content, file_path):
    buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=buffer)
    if pisa_status.err:
        return None, f'Error generating PDF: {pisa_status.err}'
    pdf = buffer.getvalue()
    buffer.close()

    # with open(file_path, 'wb') as pdf_file:
    #     pdf_file.write(pdf)
    #     print(f"PDF file '{file_path}' has been printed successfully.")

    return file_path, None

class GenerateBillView(View):
    def get(self, request, order_id):
        try:
            # Retrieve the order data
            order = OrderItem.objects.filter(order__id=order_id).first()
            if not order:
                return HttpResponse("Order not found", status=404)
            order_items = OrderItem.objects.filter(order__id=order_id)
            orders = OrderItemSerializers(order_items, many=True).data

            # Create the data for the order items table
            order_items_data = [["No", "Description", "Quantity", "Rate", "Price"]]
            for index, item in enumerate(orders, start=1):
                order_items_data.append([
                    index,
                    item['meal']['name'],
                    item['quantity'],
                    item['meal']['price'],
                    item['quantity'] * item['meal']['price']
                ])
            organization = OrganizationDetailSerializers(OrganizationDetail.objects.first(),many=False).data
            # print(organization['name'])
            # print(organization['address'])
            # print(organization['phone'])
            # Create the bill layout
            bill_data = {
                "invoice_number": order.order.id,
                "date": order.order.created_at.strftime("%d-%m-%Y"),
                "customer_name": order.order.customer.name,
                "customer_contact": f"{order.order.customer.phone}",
                "order_items": order_items_data[1:],
                "total_amount": sum(float(item['quantity'] * item['meal']['price']) for item in orders),
                "organization": OrganizationDetailSerializers(OrganizationDetail.objects.first(),many=False).data,
                "restaurant_name": "KB restaurant",
                "restaurant_address": "Kohalpur-11, Banke",
                "restaurant_contact": "9818654062, abinash@gmail.com",
            }

            # Render the bill template
            try:
                template = get_template('restaurent/bill.html')
                html = template.render({'bill_data': bill_data})
                
                # print( order_items_data[1:])
                
            except Exception as e:
                return HttpResponse(f'Error rendering template: {e}')

            # Check if the request is for HTML
            if request.GET.get('show_html') == 'true':
                return HttpResponse(html, content_type='text/html')

            # Generate the PDF
            file_path = f'bill_{order_id}.pdf'
            file_path, error = generate_pdf(html, file_path)
            if error:
                return HttpResponse(error)

        except Exception as e:
            return HttpResponse(f'Unexpected error: {e}')
        
        # return HttpResponse(f'PDF file generated and saved as {file_path}')
        return render(request, 'restaurent/bill.html', {'bill_data': bill_data})

class RefreshPageMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 200 and "/restaurant/" in request.path:
            script = """
            <script>
            function checkForUpdates() {
                fetch('/check-for-updates')
                .then(response => response.json())
                .then(data => {
                    if (data.updated) {
                        location.reload();
                    }
                })
                .catch(error => console.error('Error checking for updates:', error));
            }

            setInterval(checkForUpdates, 30000); // Check for updates every 30 seconds
            </script>
            """
            response.content = response.content.replace(b'</body>', script.encode('utf-8') + b'</body>')
        return response

SideNav=[
    
    {"name" : "Dashboard" ,"link": "restaurent/dashboard", "icons" : 'fa-solid fa-box' ,"admin":False},
    {"name" : "Floor" ,"link": "restaurent/addfloor", "icons" : 'fa-solid fa-box',"admin":False },
    {"name" : "Table " ,"link": "restaurent/addtable", "icons" : 'fa-solid fa-box',"admin":False },
    {"name" : "Category " ,"link": "restaurent/addcategory", "icons" : 'fa-solid fa-box',"admin": False },
    {"name" : "Meal Item" ,"link": "restaurent/addmeal", "icons" : 'fa-solid fa-box' ,"admin":False},
    {"name" : "Table View" ,"link": "restaurent/table", "icons" : 'fa-solid fa-box' ,"admin":False},

]


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
 
        auth_user = authenticate(request, username=username, password=password)
        if auth_user is not None:
            auth_login(request, auth_user)
            return redirect('/room')
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


def order_ready(request,order_id):
    order=get_object_or_404(OrderItem, id = order_id)
    order.is_ready=True
    order.save()

    return redirect('/restaurent/kot')


def table_view(request):
    if request.method == "POST":
        if "name" in request.POST:
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            tableId = request.POST.get("tableId")
            
            customer = Customer(name=name,phone=phone)
            customer.save()
            print(customer.id)
            return redirect(f"/restaurent/menu/{tableId}/{name}")

    context =  {
        
        "Data" : FloorSerializers(Floor.objects.all(), many=True).data,
        "OrderItem": OrderItemSerializers(OrderItem.objects.all(), many=True).data,
        
    }
    return render(request, 'restaurent/table.html',context)




def cancel_order(request,order_id,table_id,customer_name,catName=" "):
    order =get_object_or_404(OrderItem,id=order_id)
    order.delete()
    if catName == " ":
        return redirect(f"/restaurent/menu/{table_id}/{customer_name}/{catName}")
    else:
        return redirect(f"/restaurent/menu/{table_id}/{customer_name}")
    
def delete_category(request, cat_id):
    category =get_object_or_404(Category, id = cat_id)
    category.delete()
    return redirect('/restaurent/addcategory')

def delete_floor(request, floor_id):
    floor =get_object_or_404(Floor, id = floor_id)
    floor.delete()
    return redirect('/restaurent/addfloor')
            
def delete_table(request, table_id):
    order = get_object_or_404(Order, table__id = table_id)
    order.delete()
    table =get_object_or_404(TableData, id = table_id)
    table.delete()
    return redirect('/restaurent/addtable')
            
# def delete_table(request,table_id):
#     table =get_object_or_404(TableData,id=table_id)
#     table.delete()
#     return redirect('/restaurent/addtable')

def delete_meal(request, meal_id):
    meal =get_object_or_404(MealItem, id = meal_id)
    meal.delete()
    return redirect('/restaurent/addmeal')
            
def table_details(request,table_id):
    table =get_object_or_404(TableData,id=table_id)
    serializer=TableDataSerializers(table)
    return JsonResponse(serializer.data,safe=False )

def view_table_details(request,table_id):
    order = Order.objects.filter(table__id=table_id).first()
    
    # order_items = OrderItem.objects.filter(order__id=order.id)
    serializer = OrderSerializers(order, many=False)
    
    
    # total_price = sum(float(item['price']) for item in OrderItemSerializers(order_items, many=True).data )
    return JsonResponse(serializer.data,safe=False )


def add_table_view(request):
    if request.method == "POST":
        if 'search' in request.POST:
            search = request.POST.get("search", "")
            if search:
                context ={
                   "SideNav":SideNav,
                    "Data" : TableDataSerializers(TableData.objects.filter(Q(name__contains=search) ), many=True).data,
                    "Floor":FloorSerializers(Floor.objects.all(), many=True).data,

                    "Fields" : ["SN","Table Number"],
                    "Page" :"Table",
                    }
                return render(request, "room.html", context)
        if "name" in request.POST:
            name =  request.POST.get('name')
            floor = Floor.objects.filter(name = request.POST.get('floor')).first()
            occupied = False
            table = TableData(name=name,floor =floor ,occupied=occupied)
            table.save()

            return redirect('/restaurent/addtable')

        if "tableId" in request.POST:
            id =  request.POST.get('tableId')
            name =  request.POST.get('table')
            floor = Floor.objects.filter(name = request.POST.get('floor')).first()


            table = get_object_or_404(TableData,id=id)
            table.name = name
            table.floor = floor
            table.occupied = False
            table.save()

            return redirect('/restaurent/addtable')
    context ={
        "SideNav":SideNav,
        "Data":TableDataSerializers(TableData.objects.all(), many=True).data,
        "Floor":FloorSerializers(Floor.objects.all(), many=True).data,
        "Fields" : ["SN","Table Number"],
        "Page" :"Table",
    }
    return render(request, 'restaurent/addtable.html',context)

def add_floor_view(request):
    if request.method == "POST":
        if 'search' in request.POST:
            search = request.POST.get("search", "")
            if search:
                context ={
                   "SideNav": SideNav,
                    "Data" : FloorSerializers(Floor.objects.filter(Q(name__contains=search) ), many=True).data,
                    "Fields" : ["SN","Floor Name"],
                    "Page" :"Floor",
                    }
                return render(request, "room.html", context)
        if "name" in request.POST:
            name =  request.POST.get('name')

            floor = Floor(name=name)
            floor.save()

            return redirect('/restaurent/addfloor')
        
        if "floorId" in request.POST:
            name =  request.POST.get('floor')
            id =  request.POST.get('floorId')

            floor = get_object_or_404(Floor,id=id)
            floor.name = name
            floor.save()

            return redirect('/restaurent/addfloor')
    context ={
        "SideNav":SideNav,
        "Data":FloorSerializers(Floor.objects.all(), many=True).data,
        "Fields" : ["SN","Floor Name"],
        "Page" :"Floor",
    }
    return render(request, 'restaurent/addfloor.html',context)



def add_category_view(request):
    if request.method == "POST":
        if 'search' in request.POST:
            search = request.POST.get("search", "")
            if search:
                context ={
                   "SideNav":SideNav,
                    "Data" : CategorySerializers(Category.objects.filter(Q(name__contains=search) ), many=True).data,
                    "Fields" : ["SN","Category Name"],
                    "Page" :"Category",
                    }
                return render(request, "room.html", context)
    if "name" in request.POST:
        name =  request.POST.get('name')
        
        category = Category(name=name)
        category.save()

        return redirect('/restaurent/addcategory')
    if "categoryId" in request.POST:
        name =  request.POST.get('category')
        id =  request.POST.get('categoryId')
        
        category = get_object_or_404(Category,id=id)
        category.name = name
        category.save()

        return redirect('/restaurent/addcategory')
    context ={
        "SideNav":SideNav,
        "Data":CategorySerializers(Category.objects.all(), many=True).data,
        "Fields" : ["SN","Category Name"],
        "Page" :"Category",
    }
    return render(request, 'restaurent/addcategory.html',context)

def add_meal_view(request):
    if request.method == "POST":
        if 'search' in request.POST:
            search = request.POST.get("search", "")
            if search:
                context ={
                   "SideNav": SideNav,
                    "Data" : MealItemSerializers(MealItem.objects.filter(Q(name__contains=search) ), many=True).data,
                    "Fields" : ["SN","Name","Category","Price"],
                    "Page" :"MealItem",
                    }
                return render(request, "room.html", context)
    if "name" in request.POST:
        name =  request.POST.get('name')
        category = Category.objects.filter(name = request.POST.get('category')).first()
        ingredients =request.POST.get('ingredients')
        price =request.POST.get('price')
        if 'image' in request.FILES:
            image = request.FILES['image']
        
            meal = MealItem(
                name=name,
                category =category,
                image =image,
                ingredients =ingredients,
                price=price,
                )
            meal.save()
            return redirect('/restaurent/addmeal')
    
    if "mealId" in request.POST:
        id =  request.POST.get('mealId')
        name =  request.POST.get('meal')
        category = Category.objects.filter(name = request.POST.get('category')).first()
        ingredients =request.POST.get('ingredients')
        price =request.POST.get('price')
        if 'updatedimage' in request.FILES:
            image = request.FILES['updatedimage']
            
        
            meal = get_object_or_404(MealItem,id=id)
            meal.name = name
            meal.category =category
            meal.image =image
            meal.ingredients =ingredients
            meal.price=price
            meal.save()

            return redirect('/restaurent/addmeal')
    context ={
        "SideNav":SideNav,
        "Data":MealItemSerializers(MealItem.objects.all(), many=True).data,
        "Category":CategorySerializers(Category.objects.all(), many=True).data,
        "Fields" : ["SN","Name","Category","Price"],
        "Page" :"MealItem",
    }
    return render(request, 'restaurent/addmeal.html',context) 
    

def menu_by_view(request,table_id,customer_name,catName=None):
    if request.method == "POST":
        if "search" in request.POST:
            search = request.POST.get("search", "")
            if search:
                meal_items_query = MealItem.objects.filter(
                    Q(name__contains=search) | Q(price__contains=search) | Q(category__name__contains=search)
                )
                context = {
                    "SideNav": SideNav,
                    "Search": MealItemSerializers(meal_items_query, many=True).data,
                    "Nav": CategorySerializers(Category.objects.all(), many=True).data,
                    "table": table_id,
                    "customer": customer_name,
                }
                return render(request, "restaurent/menu.html", context)
          
    # customer = get_object_or_404( Customer, name = customer_name)
    # customer = Customer.objects.filter(name=customer_name).first()
    
    # table=TableData.objects.filter(id=table_id).first()

    try:
        table_occupied = get_object_or_404(TableData, id= table_id)
        table_occupied.occupied = True
        table_occupied.save()  
        order = Order.objects.filter(
            customer=Customer.objects.filter(name=customer_name).first(),
            table=TableData.objects.filter(id=table_id).first(),
        ).first()
        if order:
            order_id = order.id
            print(order_id)
        else:
            save_order = Order(
                customer=Customer.objects.filter(name=customer_name).first(),
                table=TableData.objects.filter(id=table_id).first(),
            )
            save_order.save()
            order = save_order  # Assign the new order to the order variable

    finally:
        if order:  # Check if order is not None
            order_items = OrderItem.objects.filter(order__id=order.id)
            
        else:
            return redirect("/restaurent/table")
    

    if request.method == "POST":
        if "quantity" in request.POST:
            meal =MealItem.objects.filter(name =request.POST.get("name")).first()
            quantity = request.POST.get("quantity")
           
            price = request.POST.get("price")
            
            orderItem =OrderItem(
                meal = meal,
                price = price,
                quantity = quantity,
                order = order,
                is_ready = False,
            )
            orderItem.save()
            if catName:
                return redirect(f"/restaurent/menu/{table_id}/{customer_name}/{catName}")
            else:
                return redirect(f"/restaurent/menu/{table_id}/{customer_name}")
    # print(OrderItemSerializers(order_items, many=True).data )
    total_price = sum(float(item['price']) for item in OrderItemSerializers(order_items, many=True).data)
    
    all_ready = all(item.is_ready for item in order_items)
    
    if all_ready:
        result = True
    else:
        result = False
        
        
    if catName:
        context ={
            "SideNav":SideNav,
            "Data":CategorySerializers(Category.objects.filter(name= catName).first(), many=False).data,
            "Nav":CategorySerializers(Category.objects.all(), many=True).data,
            "table":table_id,
            "table_name":table_occupied.name,
            "customer":customer_name,
            "Order":OrderItemSerializers(order_items, many=True).data,
            "Total":total_price,
            "Category":catName,
            "AllReady": result,

        }
    else:
        context ={
            "SideNav":SideNav,
            "Meal":MealItemSerializers(MealItem.objects.all(), many=True).data,
            "Nav":CategorySerializers(Category.objects.all(), many=True).data,
            "table":table_id,            
            "table_name":table_occupied.name,
            "customer":customer_name,
            "Order":OrderItemSerializers(order_items, many=True).data,
            "Total":total_price,
            "Category":catName,
            "AllReady": result,


        }
    
    return render(
        request,
        "restaurent/menu.html",
        context,
    ) 

def kot_view(request):
    order_items = OrderItemSerializers(OrderItem.objects.all(), many=True).data

    separated_data = defaultdict(list)

    for entry in order_items:
        if entry['order']['table']['id']:
            table_id = entry['order']['table']['id']
            separated_data[table_id].append(entry)

    separated_list = [{"item": items} for table_id, items in separated_data.items()]
 
    context={
        "SideNav":SideNav,
        "Data":separated_list,
    }
    return render(
        request,
        "restaurent/kot.html",
        context,
    )    
    
    

    
def restaurent_dashboard_view(request):  
    restaurent_status, created = OrganizationDetail.objects.get_or_create()

    totalbill= BillReport.objects.aggregate(Sum('total_bill'))['total_bill__sum'] or 0
    restaurent_status.total_revenue = totalbill
    restaurent_status.save()
    
    context ={
        "SideNav" : SideNav,
        # "Data" : HotelReservationSerializers(HotelReservation.objects.order_by('created_at'), many=True).data,
    #     "Reserved":RoomSerializers(Room.objects.filter(Q(status=True)), many=True ).data,
    #     "Available":RoomSerializers(Room.objects.filter(Q(status=False)), many=True ).data,
    #     "Booked":RoomSerializers(Room.objects.filter(Q(check_in_status=True)), many=True ).data,
    #     "Room":RoomSerializers(Room.objects.all(), many=True ).data,
    #     "Staff":EmployeeSerializers(Employee.objects.all(), many=True ).data,
    #     "Complaint":ComplaintSerializers(Complaint.objects.all(), many=True ).data,
    #     "PendingComplaint":ComplaintSerializers(Complaint.objects.filter(Q(resolve=False)), many=True ).data,
    #     "Customer":CustomerSerializers(Customer.objects.all(), many=True ).data,
        "OrganizationDetail":OrganizationDetailSerializers(OrganizationDetail.objects.first(), many=False ).data,
    #     "Page" :"DashBoard",
    }
    return render(
        request,
        'restaurent/dashboard.html',
        context,
    )