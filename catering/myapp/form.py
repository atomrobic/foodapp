from django import forms
from myapp.models import CateringOrder, MenuItem,Category,FoodName

class CateringOrderForm(forms.ModelForm):
    menu_items = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Allow users to select multiple menu items
        required=True
    )
    event_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))  # Date picker

    class Meta:
        model = CateringOrder
        fields = ["event_type", "event_date", "quantity", "menu_items", "address", "special_requests"]
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