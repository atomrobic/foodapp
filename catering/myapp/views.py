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


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role", "customer")

        print(f"Received -> Username: {username}, Email: {email}, Role: {role}")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        if role == "admin" and not request.user.is_superuser:
            messages.error(request, "Only superusers can create admin accounts.")
            return redirect("register")

        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            print(f"User Created: {user.username}")

            user.role = role
            user.save()

            # Authenticate & login user
            user = authenticate(request, username=username, password=password)
            if user is None:
                user = get_user_model().objects.get(username=username)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)

            messages.success(request, "Signup successful!")
            print("Redirecting to login page...")
            return redirect("login")  # Ensure this matches URLs

        except Exception as e:
            print(f"Error Creating User: {e}")
            messages.error(request, "Something went wrong. Try again.")
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

def user_login(request):
    form = AuthenticationForm(request, data=request.POST) if request.method == "POST" else AuthenticationForm()

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                
                # Debugging output
                print(f"User {user.username} authenticated successfully. Is Superuser: {user.is_superuser}")

                # Check if user is an admin
                if user.is_superuser:
                    return redirect("admin_catering_orders")  # Ensure 'adminorders' exists in urls.py
                else:
                    return redirect("catering_home")  # Ensure 'catering_home' exists in urls.py

            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")

    return render(request, "login.html", {"form": form})


# User Logout View
@login_required
def user_logout(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"}, status=200)


# Get User Profile
@login_required
def user_profile(request):
    user = request.user
    return JsonResponse({
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "phone": user.phone,
        "address": user.address,
    })


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
from .models import CateringOrder,Category,MenuItem
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import CateringOrder, OrderItem  # Ensure you import both models

from django.shortcuts import render
from .models import Order, CateringOrder

from django.shortcuts import render
from .models import Order, CateringOrder



def order_list(request):
    catering_orders = CateringOrder.objects.all()
    cart_orders = Order.objects.all()

    # Add an 'order_type' attribute for template filtering
    for order in catering_orders:
        order.order_category = "catering"
    
    for order in cart_orders:
        order.order_category = "cart"

    # Combine both querysets
    orders = list(catering_orders) + list(cart_orders)

    return render(request, "order_list.html", {"orders": orders})


from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Order, CateringOrder


def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # If using CateringOrder, change this logic
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in ["pending", "confirmed", "cancelled"]:
            order.status = new_status
            order.save()
    return redirect("order_list")

def menu_items_view(request):
    """ View to display menu items with photos and prices """
    menu_items = MenuItem.objects.all()
    return render(request, "menu_list.html", {"menu_items": menu_items})



# Function to check if user is an admin
def is_admin(user):
    return user.is_staff 

# def add_menu_item(request):
#     categories = Category.objects.all()  # Fetch all categories
#     selected_category = request.GET.get("category", "all")  # Get selected category from request

#     # Ensure selected_category is an integer (or 'all')
#     if selected_category.isdigit():
#         menu_items = MenuItem.objects.filter(category__id=int(selected_category))  # Filter by category
#     else:
#         menu_items = MenuItem.objects.all()  # Fetch all menu items

#     if request.method == "POST":
#         form = MenuItemForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect(request.path)  # ✅ Preserve category filter after adding

#     else:
#         form = MenuItemForm()

#     return render(request, "add_foods.html", {
#         "form": form,
#         "menu_items": menu_items,
#         "categories": categories,
#         "selected_category": selected_category,  # ✅ Pass selected category to template
#     })

# def add_menu_item(request):
#     categories = Category.objects.all()  # Fetch all categories

#     if request.method == "POST":
#         form = MenuItemForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("add_menu_item")  # Reload the page after saving
#     else:
#         form = MenuItemForm()

#     menu_items = MenuItem.objects.all()  # Fetch all menu items from the database
#     return render(request, "add_foods.html", {
#         "form": form,
#         "menu_items": menu_items,
#         "categories": categories,  # ✅ Pass categories to the template
#         })

from django.shortcuts import render, redirect
from .models import Category, MenuItem, FoodName


from django.shortcuts import render, redirect
from .models import Category, MenuItem
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import MenuItem, Category
from .form import CombinedMenuFoodForm

# def add_menu_item(request):
#     categories = Category.objects.all()
#     menu_items = MenuItem.objects.all()

#     combined_form = CombinedMenuFoodForm(request.POST or None, request.FILES or None)

#     if request.method == "POST":
#         if combined_form.is_valid():
#             combined_form.save()
#             return redirect("add_menu_item")  # Reload page after saving
#         else:
#             print("Form Errors:", combined_form.errors)  # Debugging

#     return render(request, "add_foods.html", {
#         "combined_form": combined_form,
#         "menu_items": menu_items,
#         "categories": categories,
#     })
    
    
from django.shortcuts import render, redirect
from .models import Category, MenuItem
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
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, MenuItem
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import CartItem
from decimal import Decimal

def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated

    # Fetch cart items only for the logged-in user
    cart_items = CartItem.objects.filter(cart__customer=request.user)

    tax_rate = Decimal('0.10')  # Example tax rate (10%)

    # Calculate subtotal (total price for all items in the cart)
    subtotal = sum(item.menu_item.price * item.quantity for item in cart_items) if cart_items else Decimal('0.00')

    # Calculate tax and total amount
    tax = subtotal * tax_rate
    total = subtotal + tax

    return render(request, 'add_cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total
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


# def menu_detail(request, item_id):
#     category_item = get_object_or_404(Category, id=item_id)
#     # menu_item = MenuItem.objects.filter(category =category_item )
    
#     categories = Category.objects.all()

#     # Get selected category from query parameters
#     category_id = request.GET.get("category", "all")

#     if category_id != "all" and category_id.isdigit():
#         filtered_items = MenuItem.objects.filter(category_id=category_id)
#     else:
#         filtered_items = MenuItem.objects.all()


#     return render(request, "category_detail.html", {
#         "filtered_items": filtered_items,
#         "category_item":category_item,
#         "categories":categories
#         })
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

def checkout(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        zipcode = request.POST.get("zipcode")
        country = request.POST.get("country")

        # Get user cart
        cart = Cart.objects.filter(customer=request.user).first()
        if not cart or not cart.cart_items.exists():
            return redirect("cart")  # Redirect if cart is empty

        # Save address
        delivery_address = DeliveryAddress.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            city=city,
            zipcode=zipcode,
            country=country
        )

        # Create an order
        order = Order.objects.create(
            customer=request.user,
            delivery_address=delivery_address,  # ✅ Set the delivery address
            total_price=cart.calculate_total_price()
        )

        # Transfer cart items to order
        for item in cart.cart_items.all():
            order.order_items.create(menu_item=item.menu_item, quantity=item.quantity, price=item.get_total_price())

        # Clear cart
        cart.cart_items.all().delete()

        return redirect("order_success", order_id=order.id)  # ✅ Pass order_id

    return render(request, "checkout.html")


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

from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Category

# def menu_item_detail(request, item_id):
#     # Get the selected menu item
#     menu_item = get_object_or_404(MenuItem, id=item_id)

#     # Get all categories for filtering dropdown
#     categories = Category.objects.all()

#     # Get selected category from query parameters (if any)
#     selected_category_id = request.GET.get('category', 'all')

#     # Filter menu items based on category
#     if selected_category_id == "all":
#         filtered_items = MenuItem.objects.all().exclude(id=menu_item.id)
#     else:
#         filtered_items = MenuItem.objects.filter(category__id=selected_category_id).exclude(id=menu_item.id)

#     # Get similar items (from the same category)
#     related_items = MenuItem.objects.filter(category=menu_item.category).exclude(id=menu_item.id)[:5]

#     context = {
#         'menu_item': menu_item,
#         'categories': categories,
#         'selected_category': selected_category_id,
#         'filtered_items': filtered_items,
#         'related_items': related_items,
#     }
#     return render(request, 'details.page.html', context)

# # def menu_detail(request, item_id):
# #     """Displays details of a specific menu item."""
# #     menu_item = get_object_or_404(MenuItem, id=item_id)
# #     return render(request, "details_page.html", {"menu_item": menu_item})

# def menu_detail(request, item_id):
#     """View to display menu items of a specific category"""
    
#     # Ensure category exists
#     category_item = get_object_or_404(Category, id=item_id)
    
#     # Get all categories for dropdown
#     categories = Category.objects.all()

#     # Get only menu items belonging to this category
#     filtered_items = MenuItem.objects.filter(category=category_item)

#     return render(request, "details_page.html", {  
#         "filtered_items": filtered_items,
#         "category_item": category_item,  # ✅ Ensure this is passed
#         "categories": categories
#     })
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import MenuItem, Category

def menu_item_detail(request, item_id):
    """Displays details of a specific menu item and filters items by category."""
    menu_item = get_object_or_404(MenuItem, id=item_id)
    categories = Category.objects.all()

    # Get selected category from query parameters
    category_id = request.GET.get("category", "all")

    if category_id and category_id.isdigit():
        filtered_items = MenuItem.objects.filter(category_id=category_id)
    else:
        filtered_items = MenuItem.objects.all()

    # Get count from request (default is 1)
    user_count = int(request.GET.get("count", 1))

    # Calculate total price
    total_price = (menu_item.price or 0) * user_count

    # Fetch 3 related items from the same category (excluding the current item)
    related_items = MenuItem.objects.filter(category=menu_item.category).exclude(id=menu_item.id)[:3] if menu_item.category else []

    return render(
        request,
        "details_page.html",
        {
            "menu_item": menu_item,
            "categories": categories,
            "filtered_items": filtered_items,
            "selected_category": category_id,
            "user_count": user_count,
            "total_price": total_price,
            "related_items": related_items,  # Pass related items to template
        },
    )

from django.shortcuts import render
from .models import Category  # Ensure correct model

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
