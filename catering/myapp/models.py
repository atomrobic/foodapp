from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now  # Import now() correctly

class CustomUser(AbstractUser):
    ADMIN = "admin"
    CUSTOMER = "customer"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (CUSTOMER, "Customer"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CUSTOMER)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
      
     
    def save(self, *args, **kwargs):
        if self.is_superuser:  # Ensure superuser is always an admin
            self.role = "admin"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="customer_profile")
    created_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=15, blank=True, null=True)  # Phone number
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Track total spending
    
    
    def update_total_spent(self):
        """Recalculate and update total spending from related orders."""
        from myapp.models import Order  # Import here to avoid circular imports
        total = Order.objects.filter(customer=self.user).aggregate(total=models.Sum("total_price"))["total"] or 0
        self.total_spent = total
        self.save()

    def __str__(self):
        return f"{self.user.email} - {self.phone if self.phone else 'No Phone'} - ${self.total_spent}"
    
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="menu_items/", blank=True, null=True)


    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class FoodName(models.Model):  
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="food_names")  # Category as FK

    def __str__(self):
        return self.name
    
    
class MenuItem(models.Model):
    name = models.ForeignKey(FoodName, on_delete=models.CASCADE, related_name="menu_items")  # Linked to FoodName
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="menu_items/", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="menu_items")
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add price field
    count = models.PositiveIntegerField(default=1)  # Food count for availability
   
    def __str__(self):
        return f"{self.name} ({'Available' if self.available else 'Not Available'})"
class DeliveryAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="addresses")  # Linked to user
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)  
    phone = models.CharField(max_length=15, blank=True, null=True)


    def __str__(self):
        return f"{self.full_name} - {self.address} - {self.zipcode}"  
class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL, null=True, blank=True)
    order_type = models.CharField(max_length=50)  # Add this field
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def can_cancel(self):
        """Check if the order was created within the last 15 minutes"""
        if self.ordered_at:  # ✅ Check if ordered_at is not None
            return (now() - self.ordered_at).total_seconds() < 900  # 900 sec = 15 min
        return False
    
def get_delivery_address(self):
    if self.customer and hasattr(self.customer, "address"):
        return self.customer.address
    return "No address available"

def save(self, *args, **kwargs):
        """Override save to update total_spent in Customer."""
        super().save(*args, **kwargs)
        self.customer.update_total_spent()  # ✅ Automatically updates total spent

def __str__(self):
        return f"Order {self.id} - {self.customer.user.email} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Make sure this field is present

def get_customer_address(self):
    if self.order and self.order.customer:  # Ensure both order and customer exist
        return self.order.customer.address
    return "No address available"  # Avoid NoneType error

from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # ✅ Ensure this field exists
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

 
class Cart(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="cart", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total_price(self):
        """Calculate the total price of all items in the cart"""
        return sum(item.get_total_price() for item in self.cart_items.all())

    def __str__(self):
        return f"Cart - {self.customer.username} ({self.id})"
    
    
  
    
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        """Calculate total price for this item"""
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} in Cart {self.cart.id}"



class FoodItemcatering(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Food item name
    description = models.TextField(blank=True, null=True)  # Optional description
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit
    is_available = models.BooleanField(default=True)  # Availability status
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price_per_unit}"

class CateringOrder(models.Model):
    EVENT_TYPES = [
        ("wedding", "Wedding"),
        ("birthday", "Birthday"),
        ("corporate", "Corporate Event"),
        ("House farming", "House farming"),
        ("other event","other event"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="catering_orders")
    name = models.CharField(max_length=255, default="Default Name")  # Change as needed1
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_date = models.DateField()
    food_items = models.ManyToManyField(FoodItemcatering)  # Linking to the new FoodItem model

    photo = models.ImageField(upload_to="order_photos/", null=True, blank=True)
    quantity = models.PositiveIntegerField()
    address = models.TextField(help_text="Event venue or delivery location")  # New field for delivery location
    special_requests = models.TextField(blank=True, null=True)  # Optional field for additional instructions
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Calculate based on menu items
    order_type = models.CharField(max_length=50)  # Add this field

    def calculate_total_price(self):
        """Calculate the total price based on selected menu items and quantity"""
        total = sum(item.price for item in self.menu_items.all()) * self.quantity
        self.total_price = total
        self.save()

    def __str__(self):
        return f"{self.customer.username} - {self.event_type} on {self.event_date} ({self.status})"


