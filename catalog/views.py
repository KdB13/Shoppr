from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import User, Product, Vendor
from .forms import RegisterForm, LoginForm, VendorLoginForm, VendorRegisterForm

# Create your views here.
def index(request):
    if "user" in request.session:
        return HttpResponseRedirect(reverse("catalog:products"))
    else:
        return render(request, 'catalog/index.html')


def login(request):
    # Redirect, if already logged in.
    if "user" in request.session:
        return HttpResponseRedirect(reverse("catalog:products"))

    if request.method == "POST":
        form = LoginForm(request.POST, auto_id=False)

        if form.is_valid():
            user = are_credentials_valid(
                form.cleaned_data["email"], 
                form.cleaned_data["password"],
                User)
            if user:
                # Create a session
                request.session["user"] = user.id
                return HttpResponseRedirect(reverse("catalog:products"))
            else:
                messages.error(request, "Incorrect email or password!")
        else:
            messages.error(request, "Invalid form!")
    else:
        form = LoginForm(auto_id=False)

    return render(request, "catalog/login.html", {"form": form})


def logout(request):
    try:
        del request.session["user"]
    except KeyError:
        pass
    return HttpResponseRedirect(reverse("catalog:index"))


def register(request):
    # Redirect, if already logged in.
    if "user" in request.session:
        return HttpResponseRedirect(reverse("catalog:products"))

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            # Save the form data
            form.save()

            # Redirect to Login page
            messages.success(request, "Registration complete! Login to continue.")
            return HttpResponseRedirect(reverse("catalog:login"))
    else:
        form = RegisterForm(auto_id=False)

    return render(request, "catalog/register.html", {"form": form})


def are_credentials_valid(email, password, model):
    result = model.objects.filter(email=email)

    # Check if a user with submitted email exists or not
    if result:
        user = result.first()

        # Check if password is valid
        if user.password == password:
            return user
        else:
            return False
    else:
        # Invalid email address
        return False


# Generic class-based views
class ProductListView(ListView):
    queryset = Product.objects.order_by("title")

    def dispatch(self, request, *args, **kwargs):
        if not "user" in request.session:
            return HttpResponseRedirect(reverse("catalog:index"))
        else:
            return super().dispatch(request, *args, **kwargs)


class ProductDetailView(DetailView):
    model = Product

    def dispatch(self, request, *args, **kwargs):
        if not "user" in request.session:
            return HttpResponseRedirect(reverse("catalog:index"))
        else:
            return super().dispatch(request, *args, **kwargs)


class ProductSearchView(ListView):
    model = Product
    template_name = "catalog/search.html"

    def get_queryset(self):
        # Get the query string
        q = self.request.GET.get('q', '')

        if q:
            query = Q(title__icontains=q) | Q(description__icontains=q) | Q(price__icontains=q)
            return self.model.objects.filter(query)
        else:
            return None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not "user" in request.session:
            return HttpResponseRedirect(reverse("catalog:index"))
        else:
            return super().dispatch(request, *args, **kwargs)


# Vendor's product views
class VendorProductListView(ListView):
    template_name = "catalog/vendors/products.html"

    def get_queryset(self):
        vendor = Vendor.objects.get(pk=self.request.session["vendor"])
        return Product.objects.filter(vendor=vendor)

    def dispatch(self, request, *args, **kwargs):
        if not "vendor" in request.session:
            return HttpResponseRedirect(reverse("catalog:vendors-login"))
        else:
            return super().dispatch(request, *args, **kwargs)


def vendors_login(request):
    # Redirect, if already logged in.
    if "vendor" in request.session:
        return HttpResponseRedirect(reverse("catalog:vendors-products"))

    if request.method == "POST":
        form = VendorLoginForm(request.POST, auto_id=False)

        if form.is_valid():
            vendor = are_credentials_valid(
                form.cleaned_data["email"], 
                form.cleaned_data["password"],
                Vendor)
            if vendor:
                # Create a session
                request.session["vendor"] = vendor.id
                return HttpResponseRedirect(reverse("catalog:vendors-products"))
            else:
                messages.error(request, "Incorrect email or password!")
        else:
            messages.error(request, "Invalid form!")
    else:
        form = VendorLoginForm(auto_id=False)

    return render(request, "catalog/vendors/login.html", {"form": form})


def vendors_register(request):
    # Redirect, if already logged in.
    if "vendor" in request.session:
        return HttpResponseRedirect(reverse("catalog:vendor-products"))

    if request.method == "POST":
        form = VendorRegisterForm(request.POST)

        if form.is_valid():
            # Save the form data
            form.save()

            # Redirect to Login page
            messages.success(request, "Registration complete! Login to continue.")
            return HttpResponseRedirect(reverse("catalog:vendors-login"))
    else:
        form = VendorRegisterForm(auto_id=False)

    return render(request, "catalog/vendors/register.html", {"form": form})


def vendors_logout(request):
    try:
        del request.session["vendor"]
    except KeyError:
        pass
    return HttpResponseRedirect(reverse("catalog:vendors-login"))



# CRUD Views
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

class ProductBaseView(FormView):
    model = Product
    fields = ["title", "description", "stock", "price", "photo"]
    success_url = reverse_lazy("catalog:vendors-products")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["auto_id"] = False
        return kwargs


    def dispatch(self, request, *args, **kwargs):
        if not "vendor" in request.session:
            return HttpResponseRedirect(reverse("catalog:vendors-login"))
        else:
            return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class ProductCreateView(ProductBaseView, CreateView):
    template_name = "catalog/vendors/product_form.html"

    def form_valid(self, form):
        # Add the current vendor to the new product
        vendor = Vendor.objects.get(pk=self.request.session["vendor"])
        form.instance.vendor = vendor
        return super().form_valid(form)
    

class ProductUpdateView(ProductBaseView, UpdateView):
    template_name = "catalog/vendors/product_form.html"


class ProductDeleteView(ProductBaseView, DeleteView):
    template_name = "catalog/vendors/product_confirm_delete.html"


class ProfileUpdateView(UpdateView):
    model = Vendor
    fields = ["name", "email", "address", "password"]
    success_url = reverse_lazy("catalog:vendors-profile")
    template_name = "catalog/vendors/profile.html"

    def get_object(self):
        return Vendor.objects.get(pk=self.request.session["vendor"])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["auto_id"] = False
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if not "vendor" in request.session:
            return HttpResponseRedirect(reverse("catalog:vendors-login"))
        else:
            return super().dispatch(request, *args, **kwargs)