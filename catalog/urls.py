from django.urls import path, include
from . import views

app_name = "catalog"

urlpatterns = [
    # For customers
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("products/", views.ProductListView.as_view(), name="products"),
    path("products/<int:pk>", views.ProductDetailView.as_view(), name="product-details"),
    path("products/search/", views.ProductSearchView.as_view(), name="product-search"),

    # For vendors
    path("vendors/login", views.vendors_login, name="vendors-login"),
    path("vendors/logout", views.vendors_logout, name="vendors-logout"),
    path("vendors/register", views.vendors_register, name="vendors-register"),
    path("vendors/products", views.VendorProductListView.as_view(), name="vendors-products"),
    path("vendors/products/add", views.ProductCreateView.as_view(), name="vendors-add-product"),
    path("vendors/products/edit/<int:pk>", views.ProductUpdateView.as_view(), name="vendors-edit-product"),
    path("vendors/products/delete/<int:pk>", views.ProductDeleteView.as_view(), name="vendors-delete-product"),
    path("vendors/profile", views.ProfileUpdateView.as_view(), name="vendors-profile")

]