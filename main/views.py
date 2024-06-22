from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, CategoryForm, BrandForm, ProductForm, UserRoleForm, EditProfileForm, CommentForm
from .models import Category, Brand, Product, CustomUser, Comment


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    print("Método de solicitud:", request.method)  # Depuración
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print("Datos del formulario POST:", request.POST)  # Depuración
        if form.is_valid():
            print("Formulario es válido")  # Depuración
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print("Usuario autenticado:", user)  # Depuración
                login(request, user)
                return redirect('home')
            else:
                print("Error de autenticación: Usuario o contraseña incorrectos")  # Depuración
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            print("Formulario no es válido")  # Depuración
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'main/edit_profile.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'main/profile.html', {'user': request.user})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'main/category_list.html', {'categories': categories})

@login_required
def add_category(request):
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        return HttpResponseForbidden("You do not have permission to add categories.")
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'main/add_category.html', {'form': form})


def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'main/brand_list.html', {'brands': brands})

@login_required
def add_brand(request):
    if not request.user.is_superuser and request.user.role not in ['ADMIN', 'EDITOR']:
        return HttpResponseForbidden("You do not have permission to add brands.")
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('brand_list')
    else:
        form = BrandForm()
    return render(request, 'main/add_brand.html', {'form': form})



def product_list(request):
    brand_id = request.GET.get('brand')
    order_by = request.GET.get('order_by', 'price')
    
    products = Product.objects.all().order_by(order_by)
    
    if brand_id:
        products = products.filter(brand_id=brand_id)
    
    brands = Brand.objects.all()
    return render(request, 'main/product_list.html', {'products': products, 'brands': brands})


@login_required
def add_product(request):
    if not request.user.is_superuser and request.user.role not in ['ADMIN', 'EDITOR']:
        return HttpResponseForbidden("You do not have permission to add products.")
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    categories = Category.objects.all()
    return render(request, 'main/add_product.html', {'form': form, 'categories': categories})


@login_required
def manage_user_role(request):
    if not (request.user.is_superuser or request.user.role == 'ADMIN'):
        return HttpResponseForbidden("You do not have permission to manage user roles.")
    
    users = CustomUser.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)
        form = UserRoleForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_user_role')
    else:
        form = UserRoleForm()

    return render(request, 'main/manage_user_role.html', {'users': users, 'form': form})

def get_brands(request, category_id):
    category = Category.objects.get(id=category_id)
    brands = Brand.objects.filter(category=category)
    return render(request, 'main/brand_list.html', {'brands': brands, 'category': category})

def get_brands_ajax(request, category_id):
    brands = Brand.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse({'brands': list(brands)})

def get_products(request, brand_id):
    brand = Brand.objects.get(id=brand_id)
    products = Product.objects.filter(brand=brand)
    return render(request, 'main/product_list.html', {'products': products, 'brand': brand})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'main/product_detail.html', {'product': product})

def custom_permission_denied_view(request, exception=None):
    return render(request, '403.html', status=403)

def custom_page_not_found_view(request, exception=None):
    return render(request, '404.html', status=404)

def forum(request):
    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'main/forum.html', {'comments': comments})

@login_required
def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('forum')
    else:
        form = CommentForm()
    return render(request, 'main/add_comment.html', {'form': form})

def about(request):
    return render(request, 'main/about.html')