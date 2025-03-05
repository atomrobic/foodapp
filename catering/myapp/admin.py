from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, MenuItem,Banner,Customer,FoodItemcatering, Order, OrderItem, CateringOrder,FoodName,DeliveryAddress
from django.apps import AppConfig

# Custom Admin for CustomUser Model
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("role", "phone", "address")}),
    )
    list_display = ("username", "email", "role", "phone", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email", "phone")
    
@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'city', 'zipcode', 'country' ,'phone')
    search_fields = ('user__username', 'full_name', 'city', 'zipcode', 'country')
    list_filter = ('city', 'country')
    
# Admin for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

# Admin for MenuItem
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "available")
    list_filter = ("category", "available")
    search_fields = ("name", "category__name")

# Admin for Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "ordered_at", "status", "total_price" ,"delivery_address",)  # ✅ Replace 'id' with 'uuid'
    list_filter = ("status", "ordered_at")
    search_fields = ("id", "customer__username")  # ✅ Use 'uuid' instead of 'id'

from django.apps import AppConfig
from django.apps import AppConfig
from importlib import import_module


# Admin for OrderItem
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "menu_item", "quantity", "price")  # Fields to display in the admin panel
    list_filter = ("order", "menu_item")  # Filter options
    search_fields = ("order__id", "menu_item__name")  # Enable search by order ID and menu item name

class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')
# Admin for CateringOrder
class CateringOrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "event_type", "event_date", "quantity", "status")
    list_filter = ("event_type", "status")
    search_fields = ("customer__username", "event_type")
    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "address", "created_at")
    search_fields = ("user__username", "phone")
    
class FoodNameAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name", "category__name")
    
admin.site.register(Customer)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(CateringOrder, CateringOrderAdmin)
admin.site.register(FoodName, FoodNameAdmin)
admin.site.register(FoodItemcatering )

admin.site.register(Banner, BannerAdmin)


class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')  # ✅ Make sure 'description' exists in Banner model
    
    
    