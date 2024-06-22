from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('brands/', views.brand_list, name='brand_list'),
    path('brands/add/', views.add_brand, name='add_brand'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('get-brands/<int:category_id>/', views.get_brands, name='get_brands'),
    path('get-brands-ajax/<int:category_id>/', views.get_brands_ajax, name='get_brands_ajax'),
    path('get-products/<int:brand_id>/', views.get_products, name='get_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('manage-user-roles/', views.manage_user_role, name='manage_user_role'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile, name='profile'),
    path('forum/', views.forum, name='forum'),
    path('forum/add/', views.add_comment, name='add_comment'),
    path('about/', views.about, name='about'),
]
