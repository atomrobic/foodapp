from django.contrib import admin
from django.urls import path
from myapp.views import (
    register, delete_address,cancel_order, category_detail,admin_dashboard,customer_detail, checkout, save_address, profile_view, menu_view,
    menu_item_detail, menu_views, dashboard_view, get_pending_orders, user_dashboard, order_success,
    update_order_status, user_login, update_quantity, remove_item, user_logout, catering_home,
    place_catering_order, order_list, add_menu_item,admin_login, delete_menu_item, add_category, edit_menu_item,
    menu_report, add_to_cart, view_cart,cart_count
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin site URL
    path("admin/", admin.site.urls),

    # Authentication-related URLs
    path("", register, name="register"),  # User registration page
    path("login/", user_login, name="login"),  # User login page
    path("logout/", user_logout, name="logout"),  # User logout functionality

    # Catering order management URLs
    path("place-order/", place_catering_order, name="place_catering_order"),  # Place a catering order
    
    path("adminorders/", order_list, name="admin_catering_orders"),  # List of all orders for admin
    path('update-order-status/<int:order_id>/', update_order_status, name='update_order_status'),  # Update order status (admin)
    path('admindashboard/', dashboard_view, name='dashboard'),  # Admin dashboard view

    # Menu management URLs
    path('add/', add_menu_item, name='add_menu_item'),  # Default route to add a menu item
    path("menu/delete/<int:item_id>/", delete_menu_item, name="delete_menu_item"),  # Delete a menu item
    path("add-category/", add_category, name="add_category"),  # Add a new category
    path("edit-menu-item/<int:item_id>/", edit_menu_item, name="edit_menu_item"),  # Edit an existing menu item
    path("menu-report/", menu_report, name="menu_report"),  # Generate a report of menu items
    path('menu/item/<int:item_id>/', menu_item_detail, name='menu_item_details'),  # View details of a specific menu item

    # Catering home and cart-related URLs
    path("home/", catering_home, name="catering_home"),  # Home page for catering services
    path('menuitem/<int:item_id>/', menu_item_detail, name='menu_item_detail'),  # View details of a menu item
    path("cart/add/<int:item_id>/", add_to_cart, name="add_to_cart"),  # Add an item to the cart
    path('cart/', view_cart, name='cart'),  # View the shopping cart
    path('view/', menu_view, name='view'),  # View menu items (general)

    # Cart management URLs
    path('cart/update/<int:item_id>/', update_quantity, name='update_quantity'),  # Update item quantity in the cart
    path('cart/remove/<int:item_id>/', remove_item, name='remove_item'),  # Remove an item from the cart
    path("checkout/", checkout, name="checkout"),  # Checkout process
    path("order-success/<int:order_id>/", order_success, name="order_success"),  # Order success confirmation page
    path("get_pending_orders/", get_pending_orders, name="get_pending_orders"),  # Fetch pending orders (JSON response)

    # User profile and dashboard URLs
    path('user_profile/', profile_view, name='user_dashboard'),  # User profile and dashboard
    path('menu/', menu_views, name='menu'),  # View all menu items
    path("save_address/", save_address, name="save_address"),  # Save or update delivery address
    path('address/<int:pk>/delete/', delete_address, name='delete_address'),  # Delete a saved address
    path("customers/", customer_detail, name="customer_list"),  # List of all customers (admin view)
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    
    
        path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
       path("orders/cancel/<int:order_id>/", cancel_order, name="cancel_order"),

    path("admin/login/", user_login, name="admin_login"),  # Admin login page
        path("adminlogin/", admin_login, name="adminlogin"),  # Admin login page
    path("cart/count/", cart_count, name="cart_count"),  # <-- Add this line


]   

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve uploaded media files