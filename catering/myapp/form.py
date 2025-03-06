from django import forms
from myapp.models import CateringOrder, MenuItem,Category,FoodName,DeliveryAddress

from django import forms
from .models import CateringOrder, FoodItemcatering

from django import forms
from .models import CateringOrder, FoodItemcatering
from django import forms
from .models import CateringOrder, FoodItemcatering

class CateringOrderForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded-md focus:ring focus:ring-orange-300",
            "placeholder": "Enter Your Name"
        }),
        label="Full Name"
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded-md focus:ring focus:ring-orange-300",
            "placeholder": "Enter Your Phone Number"
        }),
        label="Phone Number"
    )

    menu_items = forms.ModelMultipleChoiceField(
        queryset=FoodItemcatering.objects.filter(is_available=True),
        widget=forms.CheckboxSelectMultiple(attrs={
            "class": "space-y-2 p-2 border rounded-md focus:ring focus:ring-orange-300"
        }),
        required=True,
        label="Select Catering Menu Items"
    )
    
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "w-full p-2 border rounded-md focus:ring focus:ring-orange-300",
        }),
        label="Event Date"
    )
    
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            "class": "w-full p-2 border rounded-md focus:ring focus:ring-orange-300",
            "placeholder": "Enter Quantity"
        }),
        label="Quantity"
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "w-full p-2 border rounded-md focus:ring focus:ring-orange-300",
            "placeholder": "Enter Event Address",
            "rows": 3
        }),
        label="Event Address"
    )

    special_requests = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "w-full p-2 border rounded-md focus:ring focus:ring-orange-300",
            "placeholder": "Any Special Requests?",
            "rows": 3
        }),
        required=False,
        label="Special Requests"
    )

    class Meta:
        model = CateringOrder
        fields = ["name", "phone_number", "event_type", "event_date", "quantity", "menu_items", "address", "special_requests"]


from django import forms
from .models import MenuItem



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "image"]
        
        

class CombinedMenuFoodForm(forms.ModelForm):
    food_name = forms.CharField(
        max_length=255,
        required=False,
        label="New Food Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',  # Bootstrap class
            'placeholder': 'Enter new food name'
        })
    )

    class Meta:
        model = MenuItem
        fields = ['description', 'price', 'category', 'available', 'image' ,]
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'  # Bootstrap select class
            }),
            'available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'  # Bootstrap checkbox class
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def save(self, commit=True):
        food_name_input = self.cleaned_data.get('food_name')
        category = self.cleaned_data.get('category')
        if food_name_input:
            food_name_obj, created = FoodName.objects.get_or_create(name=food_name_input, category=category)
            self.instance.name = food_name_obj  # Assign it to the MenuItem
        
        return super().save(commit)
    
    
class AddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ["full_name", "address", "city", "zipcode", "country"]