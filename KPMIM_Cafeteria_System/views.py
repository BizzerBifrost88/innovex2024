from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, Staff, Cafe, Order, Admin,Menu
from django.db.models import Q
from django.http import JsonResponse

def get_menu_price(request, menuID):
    try:
        menu = Menu.objects.get(menuID=menuID)
        return JsonResponse({'price': menu.price})
    except Menu.DoesNotExist:
        return JsonResponse({'price': 0}, status=404)

#Home Section
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = binary_search_email(User, email)
        staff = binary_search_email(Staff, email)
        admin = binary_search_email(Admin, email)

        if user:
            if user.password == password:
                request.session['user_type'] = 'user'
                request.session['user_id'] = user.userID  
                return redirect('usermenu')
            else:
                messages.error(request, "Password is incorrect.")
        elif staff:
            if staff.password == password:
                request.session['user_type'] = 'staff'
                request.session['user_id'] = staff.staffID
                return redirect('staffmenu')
            else:
                messages.error(request, "Password is incorrect.")
        elif admin:
            if admin.password == password:
                request.session['user_type'] = 'admin'
                request.session['user_id'] = admin.adminID 
                return redirect('adminmenu')
            else:
                messages.error(request, "Password is incorrect.")
        else:
            messages.error(request, "Email not found. Please sign up first.")

    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect('login')

def binary_search_email(model, email):
    try:
        return model.objects.get(email=email)
    except model.DoesNotExist:
        return None

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password == confirm_password:
            if User.objects.filter(email=email).exists() or Staff.objects.filter(email=email).exists() or Admin.objects.filter(email=email).exists():
                messages.error(request, 'The email has been taken. Please try again.')
            else:
                try:
                    user = User(name=name, email=email, phone=phone, password=password)
                    user.save()
                    messages.success(request, 'Sign up successful! You can now log in.')
                    return redirect('login')
                except Exception as e:
                    messages.error(request, 'Error occurred while signing up. Please try again.')
        else:
            messages.error(request, 'Passwords do not match. Please try again.')

    return render(request, 'signup.html')

#Admin Section
def adminmenu(request):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'admin':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')  
    return render(request, 'admin/adminMenu.html')

def cafestaff(request):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'admin':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')  
    return render(request, 'admin/cafe-staff.html')

def usersetting(request):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'admin':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')  
    if request.method=="POST":
        if request.POST.get('userID'):
            userID = request.POST.get('userID')
            if User.objects.filter(userID=userID).exists():
                try:
                    User.objects.filter(userID=userID).delete()
                    messages.success(request, 'Delete user successful')
                except Exception as e:
                    messages.error(request, 'Error occurred while deleting. Please try again.')
            else:
                messages.error(request, 'This ID does not exist. Please use a different ID.') 

    myuser=User.objects.all().values()
    context = {
        'myuser':myuser,
    }

    return render(request, 'admin/user-setting.html',context)

def cafedetail(request):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'admin':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')  
    if request.method=="POST":
        if request.POST.get('name'):
            name = request.POST.get('name')
            if Cafe.objects.filter(name=name).exists():
                messages.error(request, 'This name has been taken. Please use a different name.')
            else:
                try:
                    data = Cafe(name=name)
                    data.save()
                    messages.success(request, 'Register cafe successful')
                except Exception as e:
                    messages.error(request, 'Error occurred while registering. Please try again.')

        if request.POST.get('cafeID'):
            cafeID = request.POST.get('cafeID')
            if Cafe.objects.filter(cafeID=cafeID).exists():
                try:
                    Cafe.objects.filter(cafeID=cafeID).delete()
                    messages.success(request, 'Delete cafe successful')
                except Exception as e:
                    messages.error(request, 'Error occurred while deleting. Please try again.')
            else:
                messages.error(request, 'This ID does not exist. Please use a different ID.') 
            
            

    if not request.session.get('user_type') == 'admin':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')  

    mycafe=Cafe.objects.all().values()
    context = {
        'mycafe':mycafe,
    }
                                       
    return render(request, 'admin/cafe-detail.html',context)

def staffdetail(request):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'admin':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')  
    if request.method=="POST":
        if request.POST.get('email'):
            email = request.POST.get('email')
            if User.objects.filter(email=email).exists() or Staff.objects.filter(email=email).exists() or Admin.objects.filter(email=email).exists():
                messages.error(request, 'The email has been taken. Please try again.')
            else:
                try:
                    password=request.POST.get('password')
                    name=request.POST.get('name')
                    phone=request.POST.get('phone')
                    cafe=request.POST.get('cafeID')
                    cafe_ID = Cafe.objects.get(cafeID=cafe)
                    data = Staff(email=email, password=password, name=name, phone=phone, cafeID=cafe_ID)
                    data.save()
                    messages.success(request, 'Register staff successful')
                except Exception as e:
                    messages.error(request, 'Error occurred while registering. Please try again.')
        if request.POST.get('staffID'):
            staffID = request.POST.get('staffID')
            if Staff.objects.filter(staffID=staffID).exists():
                try:
                    Staff.objects.filter(staffID=staffID).delete()
                    messages.success(request, 'Delete cafe successful')
                except Exception as e:
                    messages.error(request, 'Error occurred while deleting. Please try again.')
            else:
                messages.error(request, 'This ID does not exist. Please use a different ID.') 

    mystaff=Staff.objects.all().values()
    context = {
        'mystaff':mystaff,
    }
    
    return render(request, 'admin/staff-detail.html',context)


#Staff Section
def staffmenu(request):
    user_id = request.session.get('user_id')
    
    if not request.session.get('user_type') == 'staff':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')  
    staff = Staff.objects.get(staffID=user_id)
    cafe = staff.cafeID
    cafe_name=cafe.name
    staff_name=staff.name
    context = {
        'cafe_name':cafe_name,
        'staff_name':staff_name,
    }
    return render(request, 'staff/staffMenu.html',context)

def orderdetail(request):
    user_id = request.session.get('user_id')

    if not request.session.get('user_type') == 'staff':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')

    if request.method == "POST":
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        
        try:
            order = Order.objects.get(orderID=order_id)
            order.status = new_status
            order.save()
            messages.success(request, f'Order {order_id} status updated successfully.')
        except Order.DoesNotExist:
            messages.error(request, 'Order does not exist.')
    staff = Staff.objects.get(staffID=user_id)
    cafe = staff.cafeID
    received_orders = Order.objects.filter(cafeID=cafe, status=0)  
    preparing_orders = Order.objects.filter(cafeID=cafe, status=1)  
    ready_orders = Order.objects.filter(cafeID=cafe, status=2) 
    
    context = {
        'received_orders': received_orders,
        'preparing_orders': preparing_orders,
        'ready_orders': ready_orders,
    }

    return render(request, 'staff/order-detail.html', context)

def menudetail(request):
    user_id = request.session.get('user_id')
    if not request.session.get('user_type') == 'staff':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')  


    staff = Staff.objects.get(staffID=user_id)
    cafe_id = staff.cafeID
  
    mymenu = Menu.objects.filter(cafeID=cafe_id)

    if request.method == "POST":
        if 'name' in request.POST and 'price' in request.POST:
            name = request.POST.get('name')
            price = request.POST.get('price')  

            if name and price:
                try:
                    price = float(price)  
                    menu_item = Menu(name=name, price=price, cafeID=cafe_id)
                    menu_item.save()
                    messages.success(request, 'Menu item added successfully.')
                except ValueError:
                    messages.error(request, 'Please enter a valid price.')
                except Exception as e:
                    messages.error(request, f"An error occurred: {e}")
            else:
                messages.error(request, 'Please provide both name and price.')

        elif 'menuID' in request.POST:
            menu_id = request.POST.get('menuID')
            try:
                menu_item = Menu.objects.get(menuID=menu_id, cafeID=cafe_id)
                menu_item.delete()
                messages.success(request, 'Menu item deleted successfully.')
            except Menu.DoesNotExist:
                messages.error(request, 'Menu item not found.')
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

    context = {
        'mymenu': mymenu
    }
    
    return render(request, 'staff/menu-detail.html', context)

#User Section
def usermenu(request):
    user_id = request.session.get('user_id')
    
    # Ensure the user is logged in as 'user'
    if not request.session.get('user_type') == 'user':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again")
        return redirect('login')  
    
    # Retrieve all cafes for selection
    mycafe = Cafe.objects.all()
    
    # Handle the cafe selection (from POST or GET)
    if request.method == 'POST':
        cafe_id = request.POST.get('cafe_id')
        if cafe_id:
            return redirect('userorder', cafe_id=cafe_id)  # Redirect to userorder view with cafe_id

    user = User.objects.get(userID=user_id)
    name = user.name
    context = {
        'mycafe': mycafe,
        'name': name,
    }
    return render(request, 'user/userMenu.html', context)

def userorder(request, cafe_id):
    user_id = request.session.get('user_id')
    
    if not request.session.get('user_type') == 'user':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again.")
        return redirect('login')
    
    # If `cafe_id` is not passed, display an error or redirect
    if not cafe_id:
        messages.error(request, "No cafe selected.")
        return redirect('usermenu')
    
    # Filter the menu by the selected cafe_id
    mymenu = Menu.objects.filter(cafeID=cafe_id)
    
    context = {
        'mymenu': mymenu,
        'cafe_id': cafe_id  # Pass cafe_id for order placement
    }

    if request.method == 'POST':
        menu_id = request.POST.get('menuID')
        quantity = request.POST.get('quantity')

        try:
            menu = Menu.objects.get(menuID=menu_id)
            user = User.objects.get(userID=user_id)  
            
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be a positive number.")

            # Create a new order
            order = Order(
                menuID=menu,
                cafeID=menu.cafeID,  # This ensures the order is linked to the selected cafe
                userID=user,
                quantity=quantity,
            )
            order.save()

            messages.success(request, "Your order has been placed successfully!")

        except Menu.DoesNotExist:
            messages.error(request, "The selected menu item does not exist.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
        except ValueError as ve:
            messages.error(request, f"Invalid input: {ve}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")

    return render(request, 'user/user-order.html', context)

def trackingorder(request):
    user_id = request.session.get('user_id')
    
    if not request.session.get('user_type') == 'user':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again.")
        return redirect('login')
    
    myorder = Order.objects.filter(userID=user_id)
    
    context = {
        'myorder': myorder,
    }
    return render(request, 'user/tracking-order.html', context)

def userprofile(request):
    user_id = request.session.get('user_id')
    
    if not request.session.get('user_type') == 'user':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again.")
        return redirect('login')
    myuser = User.objects.filter(userID=user_id)
    name = User.objects.get(userID=user_id)
    
    context={
        'myuser': myuser,
        'name': name,
    }
    return render(request,'user/user-profile.html',context)


def usercart(request):
    user_id = request.session.get('user_id')

    # Check if user is authenticated and has the correct user type
    if not request.session.get('user_type') == 'user':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again.")
        return redirect('login')

    # Retrieve the user's orders with status 2 (ready to pickup)
    data = Order.objects.filter(userID=user_id)

    if request.method == "POST":
        order_id = request.POST.get('order_id')  # Retrieve the order ID from the form

        # Get the corresponding order and update its status to 3 (for payment complete)
        try:
            order = Order.objects.get(orderID=order_id, userID=user_id)
            order.pay = 1  # Update status to 3 (Paid)
            order.save()

            messages.success(request, f"Payment for Order ID {order_id} is successful.")
        except Order.DoesNotExist:
            messages.error(request, "Order not found or already paid.")

        return redirect('usercart')  # Reload the page after the update

    context = {
        'data': data,
    }

    return render(request, 'user/user-cart.html', context)

def receipt(request):
    user_id = request.session.get('user_id')

    # Check if user is authenticated and has the correct user type
    if not request.session.get('user_type') == 'user':
        request.session.flush()
        messages.error(request, "You do not have permission to view this page. Please login again.")
        return redirect('login')

    # Retrieve the user's orders with status 2 (ready for pickup) and pay = 1 (paid orders)
    data = Order.objects.filter(userID=user_id, pay=1)  # Filter for status=2 and pay=1
    context = {
        'data': data,
    }
    return render(request, 'user/receipt.html', context)