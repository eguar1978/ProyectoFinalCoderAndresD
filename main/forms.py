import os
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Category, Brand, Product, CustomUser, Comment
from django.utils.crypto import get_random_string

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Correo electrónico ya está en uso.")
        return email
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'category']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'description', 'price', 'image']

    def save(self, commit=True):
        product = super(ProductForm, self).save(commit=False)
        if self.cleaned_data['image']:
            image = self.cleaned_data['image']
            image_name = image.name
            image_path = os.path.join('media', 'products', image_name)
            
            if os.path.exists(image_path):
                # Generar un nuevo nombre para la imagen
                new_image_name = f"{os.path.splitext(image_name)[0]}_{get_random_string(8)}{os.path.splitext(image_name)[1]}"
                product.image.name = new_image_name
            
        if commit:
            product.save()
        return product

class UserRoleForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['role']

class EditProfileForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']