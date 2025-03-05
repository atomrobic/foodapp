from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json
from myapp.models import CustomUser  # Replace 'app' with your actual app name
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import MenuItem



CustomUser = get_user_model()


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser  # Ensure this is the correct user model

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser  # Ensure your CustomUser model has a 'role' field

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import CustomUser, Customer

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .models import CustomUser  # Removed Customer model import


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model

User = get_user_model()
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .models import CustomUser, Customer

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        phone = request.POST.get("phone", "")  # Get phone number from form

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        try:
            # Create User
            user = CustomUser.objects.create_user(username=username, email=email, password=password)

            # Create Customer entry
            Customer.objects.create(user=user, phone=phone)

            # Authenticate and log in the user
            user = authenticate(request, username=username, password=password ,customer=Customer)
            if user:
                login(request, user)

            messages.success(request, "Signup successful!")
            return redirect("login")  # Redirect to home or dashboard

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect("register")

    return render(request, "register.html")


from django.shortcuts import render
from django.db.models import Sum
from .models import CustomUser, Order

def dashboard_view(request):
    total_users = CustomUser.objects.count()  # Count total users
    total_orders = Order.objects.count()  # Count total orders
    catering_orders = Order.objects.filter(order_type="catering").count()  # Filter catering orders
    total_amount = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0  # Sum total amount

    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_amount': total_amount,
        'avg_time_spent': "15 min",  # Example value, replace with actual logic
    }
    return render(request, 'admin_panel.html', context)


# Get all users



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Check if the user is an admin
            if user.is_staff or user.is_superuser:
                messages.success(request, 'Successfully logged in! Welcome, Admin.')
                return redirect('dashboard')  # Redirect to the dashboard for admins
            else:
                messages.success(request, 'Successfully logged in! Welcome.')
                return redirect('catering_home')  # Redirect to the catering home page for regular users
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  # Redirect back to the login page with an error message
    
    return render(request, 'login.html')

# User Logout View
@login_required
def user_logout(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"}, status=200)




from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Customer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Customer

from django.shortcuts import render, get_object_or_404
from .models import Customer, Order

from django.shortcuts import render, get_object_or_404
from .models import Customer


def customer_detail(request):
    # Get all customers
    customers = Customer.objects.all()

    # Prepare the data for the template
    context = {
        "customers": customers,
    }

    return render(request, "customer_data.html", context)
# # Get User Profile
# @login_required
# def user_profile(request):
#     user = request.user
#     return JsonResponse({
#         "username": user.username,
#         "email": user.email,
#         "role": user.role,
#         "phone": user.phone,
#         "address": user.address,
#     })


# Update User Profile
@login_required
@csrf_exempt
def update_profile(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user

        user.phone = data.get("phone", user.phone)
        user.address = data.get("address", user.address)
        user.save()

        return JsonResponse({"message": "Profile updated successfully"}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)

from django.shortcuts import render

from django.shortcuts import render
from .models import MenuItem


# def menu_item_detail(request, item_id):
#     # Get the menu item or return 404
#     item = get_object_or_404(MenuItem, pk=item_id)
    
#     # Get related items (same category, excluding current item)
#     related_items = MenuItem.objects.filter(
#         category=item.category
#     ).exclude(pk=item_id)[:4]
    
#     # Get all categories for navigation
#     categories = Category.objects.all()
    
#     context = {
#         'item': item,
#         'related_items': related_items,
#         'categories': categories,
#     }
    
#     return render(request, 'menu_details.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .form import CateringOrderForm

@login_required
def place_catering_order(request):
    if request.method == "POST":
        form = CateringOrderForm(request.POST)
        (form)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user  # Assign the logged-in user
            order.save()
            form.save_m2m()  # Save ManyToMany field (menu_items)
            return redirect("catering_home")  # Redirect to home page after order
    else:
        form = CateringOrderForm()

    return render(request, "catering_order.html", {"form": form})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum
from .models import Order, CateringOrder



def update_order_status(request, order_id):
    """Update the status of an order (handles both CateringOrder and Order)"""
    # Fetch the order (CateringOrder or Order)
    catering_order = CateringOrder.objects.filter(id=order_id).first()
    if catering_order:
        order = catering_order
        order_type = "catering"
    else:
        order = get_object_or_404(Order, id=order_id)
        order_type = "cart"

    if request.method == "POST":
        new_status = request.POST.get("status", "").strip().capitalize()  # Normalize input
        print(f"Raw status from request: '{request.POST.get('status')}'")  # Debugging
        print(f"Normalized status: '{new_status}'")  # Debugging

        valid_statuses = ["Pending", "Processing", "Completed", "Cancelled"]
        if new_status in valid_statuses:
            order.status = new_status
            order.save()
            messages.success(request, f"{order_type.capitalize()} order status updated to {order.status}.")
        else:
            print(f"Invalid status received: '{new_status}'")  # Debugging
            messages.error(request, "Invalid status update.")

    return redirect("admin_catering_orders")
from django.db.models import Sum
from django.shortcuts import render
from .models import CateringOrder, Order

def order_list(request):
    """Fetch and display all orders (catering & cart)"""
    catering_orders = CateringOrder.objects.all()
    cart_orders = Order.objects.annotate(total_quantity=Sum('order_items__quantity'))

    # Assign order_category for template filtering
    for order in catering_orders:
        order.order_category = "catering"
        order.total_quantity = 0  # Default for catering orders

    for order in cart_orders:
        order.order_category = "cart"

    orders = list(catering_orders) + list(cart_orders)

    return render(request, "order_list.html", {"orders": orders})

def menu_items_view(request):
    """ View to display menu items with photos and prices """
    menu_items = MenuItem.objects.all()
    return render(request, "menu_list.html", {"menu_items": menu_items})



# Function to check if user is an admin
def is_admin(user):
    return user.is_staff 



from .models import Category, MenuItem
from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Category
from .form import CombinedMenuFoodForm

    
def add_menu_item(request):
    categories = Category.objects.all()
    category_id = request.GET.get("category")  # Get selected category from URL

    if category_id:
        menu_items = MenuItem.objects.filter(category_id=category_id)  # Filter by category
    else:
        menu_items = MenuItem.objects.all()  # Show all if no category is selected

    combined_form = CombinedMenuFoodForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if combined_form.is_valid():
            combined_form.save()
            return redirect("add_menu_item")  # Reload page after saving
        else:
            print("Form Errors:", combined_form.errors)  # Debugging

    return render(request, "add_foods.html", {
        "combined_form": combined_form,
        "menu_items": menu_items,
        "categories": categories,
        "selected_category": category_id,  # Pass selected category for UI updates
    })
  
def delete_menu_item(request, item_id):
    if request.method == "POST":
        menu_item = get_object_or_404(MenuItem, id=item_id)
        menu_item.delete()
        return JsonResponse({"success": True})  

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)



from django.shortcuts import render
from django.http import JsonResponse










from django.shortcuts import render, redirect
from .models import Category
from .form import CategoryForm  # Ensure 'forms' is plural

def add_category(request):
    categories = Category.objects.all()  # Fetch all categories

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("menu_detail")  # Reloads the page after saving
    else:
        form = CategoryForm()

    return render(request, "category.html", {  # Ensure correct template name
        "form": form,
        "categories": categories,
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Category
from .form import CombinedMenuFoodForm

def edit_menu_item(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)  # Fetch the item or return 404
    categories = Category.objects.all()

    if request.method == "POST":
        form = CombinedMenuFoodForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect("add_menu_item")  # Redirect after successful update
    else:
        form = CombinedMenuFoodForm(instance=menu_item)  # Pre-fill form with existing data

    return render(request, "edit_foods.html", {
        "form": form,
        "menu_item": menu_item,
        "categories": categories,
    })
import csv
from django.http import HttpResponse
from django.shortcuts import render
from .models import Category, MenuItem



def menu_report(request):
    categories = Category.objects.prefetch_related("menu_items").all()
    
    if "download_csv" in request.GET:  # Check if download button is clicked
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="menu_report.csv"'

        writer = csv.writer(response)
        writer.writerow(["Category", "Menu Item", "Price", "Availability"])

        for category in categories:
            for item in category.menu_items.all():
                writer.writerow([category.name, item.name, item.price, "Available" if item.available else "Not Available"])

        return response

    return render(request, "menu_report.html", {"categories": categories})

##########################################################################################

#user inserface

from django.shortcuts import render
from .models import MenuItem, Category, Banner  # Import your models
from django.shortcuts import render
from .models import Category, Banner, MenuItem
def catering_home(request):
    # Fetch all categories and banners
    categories = Category.objects.all()
    banners = Banner.objects.all()

    # Get category from URL parameter
    selected_category_name = request.GET.get("category")

    # Initialize variables
    menu_items = None  # To store filtered menu items for the selected category
    menu_items_by_category = {}  # To store all menu items grouped by category

    # Fetch all menu items grouped by category
    for category in categories:
        menu_items_for_category = MenuItem.objects.filter(category=category)
        menu_items_by_category[category.name] = menu_items_for_category

        # If a specific category is selected, filter menu items for that category
        if selected_category_name and category.name == selected_category_name:
            menu_items = menu_items_for_category

    # If no category is selected, show all menu items
    if not selected_category_name:
        menu_items = MenuItem.objects.all()

    # Render the template with context 
    return render(
        request,
        "home.html",
        {
            "menu_items": menu_items,  # Menu items for the selected category (or all items if none selected)
            "menu_items_by_category": menu_items_by_category,  # All menu items grouped by category
            "categories": categories,  # All categories
            "banners": banners,  # All banners
            "selected_category": selected_category_name,  # Currently selected category name
        },
    )

from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Category

# View for listing menu items by category
from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Category

from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Category



####################
#cart

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cart

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, MenuItem

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem, MenuItem
from decimal import Decimal

from django.shortcuts import render, get_object_or_404
from .models import CartItem
from decimal import Decimal


def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated

    # Fetch cart items for the logged-in user
    cart_items = CartItem.objects.filter(cart__customer=request.user)

    tax_rate = Decimal('0.10')  # Example tax rate (10%)

    # Calculate subtotal (total price for all items in the cart)
    subtotal = sum(item.menu_item.price * item.quantity for item in cart_items) if cart_items else Decimal('0.00')

    # Calculate tax and total amount
    tax = subtotal * tax_rate
    total = subtotal + tax

    # Fetch user's saved addresses (max 2)
    user_addresses = DeliveryAddress.objects.filter(user=request.user)[:2]

    return render(request, 'add_cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
        'addresses': user_addresses,  # Pass addresses to template
    })
    
def update_quantity(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()

    return redirect('cart')

def remove_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart')

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Cart, CartItem

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import MenuItem, Cart, CartItem

def add_to_cart(request, item_id):
    """Add an item to the cart using item_id from URL."""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "User not authenticated"}, status=401)

    menu_item = get_object_or_404(MenuItem, id=item_id)
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{menu_item.name} added to cart!")

    return JsonResponse({"success": True, "message": f"{menu_item.name} added to cart!"})

from django.shortcuts import render, redirect
from .models import DeliveryAddress, Order, Cart, CartItem
from django.shortcuts import redirect
from django.contrib import messages
from .models import DeliveryAddress, Order, Cart

def checkout(request):
    if request.method == "POST":
        if "delete_address" in request.POST:  # Check if delete button is clicked
            address_id = request.POST.get("delete_address")
            address = get_object_or_404(DeliveryAddress, id=address_id, user=request.user)
            address.delete()
            messages.success(request, "Address deleted successfully!")
            return redirect("checkout")

        selected_address_id = request.POST.get("selected_address")

        # Ensure cart exists
        cart = Cart.objects.filter(customer=request.user).first()
        if not cart or not cart.cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect("cart")

        # Ensure an address is selected
        if not selected_address_id:
            messages.error(request, "Please select a delivery address.")
            return redirect("checkout")

        # Get the selected address
        delivery_address = get_object_or_404(DeliveryAddress, id=selected_address_id, user=request.user)

        # Create order
        total_price = sum(item.get_total_price() for item in cart.cart_items.all())  # Ensure `get_total_price()` exists
        order = Order.objects.create(
            customer=request.user,
            delivery_address=delivery_address,
            total_price=total_price
        )

        # Transfer cart items to order
        for item in cart.cart_items.all():
            order.order_items.create(menu_item=item.menu_item, quantity=item.quantity, price=item.get_total_price())

        # Clear cart
        cart.cart_items.all().delete()

        return redirect("order_success", order_id=order.id)

    # Fetch user's saved addresses
    addresses = DeliveryAddress.objects.filter(user=request.user)
    return render(request, "checkout.html", {"addresses": addresses})



from django.contrib.auth.decorators import login_required
@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)  # ✅ Ensure order exists

    return render(request, "checkout.html", {"order": order})  # ✅ Ensure correct template


from django.http import JsonResponse

def get_pending_orders(request):
    catering_pending_orders = CateringOrder.objects.filter(status="pending").count()
    order_pending_orders = Order.objects.filter(status="pending").count()
    
    total_pending_orders = catering_pending_orders + order_pending_orders
    
    return JsonResponse({"pending_orders": total_pending_orders})

@login_required
def user_dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')[:5]
    return render(request, 'dashboard.html', {'orders': orders})


####


def menu_items_detail(request, item_id):
    # Get the menu item or return 404
    item = get_object_or_404(MenuItem, pk=item_id)
    
    # Get related items (same category, excluding current item)
    related_items = MenuItem.objects.filter(
        category=item.category
    ).exclude(pk=item_id)[:4]
    
    # Get all categories for navigation
    categories = Category.objects.all()
    
    context = {
        'item': item,
        'related_items': related_items,
        'categories': categories,
    }
    
    return render(request, 'menu_details.html', context)
###################

from .models import MenuItem, Category




def menu_item_detail(request, item_id):
    """Displays details of a specific menu item with filtering by price and category."""
    menu_item = get_object_or_404(MenuItem, id=item_id)
    categories = Category.objects.all()

    # Get selected category & price from query params
    category_id = request.GET.get("category", "all")
    price_range = request.GET.get("price", "")

    # Filtering by category
    if category_id.isdigit():
        filtered_items = MenuItem.objects.filter(category_id=category_id).exclude(id=menu_item.id)
    else:
        filtered_items = MenuItem.objects.exclude(id=menu_item.id)

    # Filtering by price
    if price_range:
        if price_range == "0-500":
            filtered_items = filtered_items.filter(price__lte=500)
        elif price_range == "501-1000":
            filtered_items = filtered_items.filter(price__gt=500, price__lte=1000)
        elif price_range == "1001-2000":
            filtered_items = filtered_items.filter(price__gt=1000, price__lte=2000)
        elif price_range == "2001-5000":
            filtered_items = filtered_items.filter(price__gt=2000, price__lte=5000)
        elif price_range == "5001+":
            filtered_items = filtered_items.filter(price__gt=5000)

    return render(
        request,
        "details_page.html",
        {
            "menu_item": menu_item,
            "categories": categories,
            "filtered_items": filtered_items,
        },
    )


from django.shortcuts import render
from .models import Category  # Ensure correct model
from django.shortcuts import render

def category_detail(request, category_id):
    return render(request, 'category_detail.html', {'category_id': category_id})


def menu_view(request):
    categories = Category.objects.all()  # Fetch categories
    return render(request, 'details_page.html', {'categories': categories})

from django.shortcuts import render, get_object_or_404
from .models import Category, MenuItem

def menu_views(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()

    # Get the selected category from query parameters
    selected_category_id = request.GET.get('category')
    if selected_category_id:
        selected_category = get_object_or_404(Category, id=selected_category_id)
        menu_items = menu_items.filter(category=selected_category)
    else:
        selected_category = None

    context = {
        'categories': categories,
        'menu_items': menu_items,
        'selected_category': selected_category,
    }
    return render(request, 'details.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .form import AddressForm  # Assuming you have an AddressForm

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order, DeliveryAddress


from django.shortcuts import render, redirect
from .models import DeliveryAddress, Order  # Ensure you import your models
from django.shortcuts import render
from .models import DeliveryAddress, Order

def profile_view(request):
    addresses = DeliveryAddress.objects.filter(user=request.user)[:2]  # Fetch only two addresses
    recent_orders = Order.objects.filter(customer=request.user).order_by('-ordered_at')[:5]  # Fetch last 5 orders

    context = {
        'addresses': addresses,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'profile.html', context)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import DeliveryAddress


from django.shortcuts import redirect
from django.http import JsonResponse
from .models import DeliveryAddress  # Import your model

# def save_address(request):
#     if request.method == 'POST':
#         edit_index = request.POST.get('edit_index')
#         full_name = request.POST.get('full_name')  # ✅ Fix: Correct field name
#         address_text = request.POST.get('address')
#         country = request.POST.get('street')
#         city = request.POST.get('city')
#         phone = request.POST.get('phone')
#         zipcode = request.POST.get('zipcode')

#         # ✅ Fix: Validate required fields before saving
#         if not full_name:
#             return JsonResponse({"error": "Full Name is required"}, status=400)

#         if edit_index:
#             try:
#                 address_obj = DeliveryAddress.objects.get(id=edit_index, user=request.user)
#                 address_obj.full_name = full_name  # ✅ Fix: Correct field assignment
#                 address_obj.address = address_text
#                 address_obj.country = country
#                 address_obj.city = city
#                 address_obj.phone = phone
#                 address_obj.zipcode = zipcode

#                 address_obj.save()
#             except DeliveryAddress.DoesNotExist:
#                 return JsonResponse({"error": "Address not found"}, status=404)
#         else:
#             DeliveryAddress.objects.create(
#                 user=request.user,
#                 full_name=full_name,  # ✅ Fix: Ensure full_name is not missing
#                 address=address_text,
#                 country=country,
#                 city=city,
#                 phone=phone,
#                 zipcode=zipcode
#             )

#         return redirect('user_dashboard')

#     return redirect('profile')

# from django.shortcuts import get_object_or_404

# def edit_address(request, pk):
#     address = get_object_or_404(DeliveryAddress, pk=pk, user=request.user)
#     if request.method == 'POST':
#         form = AddressForm(request.POST, instance=address)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = AddressForm(instance=address)
#     return render(request, 'edit_address.html', {'form': form})
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import DeliveryAddress

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from .models import DeliveryAddress

def save_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('id')  # Use 'id' to differentiate edit vs. create
        full_name = request.POST.get('full_name')
        address_text = request.POST.get('address')
        country = request.POST.get('country')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        zipcode = request.POST.get('zipcode')

        # Ensure required fields
        if not full_name or not address_text or not city or not phone or not zipcode:
            return JsonResponse({"error": "All fields are required"}, status=400)

        # If address_id exists, update; otherwise, create new
        if address_id:
            address_obj = get_object_or_404(DeliveryAddress, id=address_id, user=request.user)
        else:
            address_obj = DeliveryAddress(user=request.user)

        # Update fields
        address_obj.full_name = full_name
        address_obj.address = address_text
        address_obj.country = country
        address_obj.city = city
        address_obj.phone = phone
        address_obj.zipcode = zipcode
        address_obj.save()

        # Determine the next page (Profile or Cart) based on request
        next_page = request.POST.get('next', 'profile')  # Default to 'profile'

        # JSON response for AJAX calls (dynamic updates)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                "success": True,
                "message": "Address saved successfully!",
                "next_page": next_page,
                "address": {
                    "id": address_obj.id,
                    "full_name": address_obj.full_name,
                    "address": address_obj.address,
                    "city": address_obj.city,
                    "zipcode": address_obj.zipcode,
                    "phone": address_obj.phone
                }
            })

        return redirect(next_page)  # Redirect based on where the request came from

    return redirect('profile')  # If not POST, go to profile


from django.contrib import messages

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import DeliveryAddress

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def delete_address(request, pk):
    address = get_object_or_404(DeliveryAddress, pk=pk, user=request.user)
    
    if request.method == 'POST':
        address.delete()
        messages.success(request, '✅ Address deleted successfully!')

    # Determine where to redirect (cart or profile)
    next_page = request.GET.get('next', 'user_dashboard')  # Default: user_dashboard
    return redirect(next_page)
