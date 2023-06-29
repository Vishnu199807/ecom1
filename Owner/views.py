from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,ListView,DetailView
from django.contrib import messages
from Owner.models import *
from django.core.mail import send_mail
from Owner.forms import OrderUpdateForm
from django.contrib.auth import authenticate,login,logout
from .forms import ProductForm
from django.views.decorators.http import require_http_methods


class SignOutView(View):
    def get(self, request, *args, **kwargs):
        print(request.user.is_authenticated)
        logout(request)
        return redirect("login")

class AdminDashBoardView(TemplateView):
    template_name = "dashboard.html"

    def form_valid(self, form):
        messages.success(self.request,"you are logged in..")
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)    # to override parent
        cnt=Orders.objects.filter(status="order-placed").count()
        context["count"]=cnt
        return context

class OrdersListView(ListView):
    model=Orders
    context_object_name = "orders"
    template_name = "owner/admin_listorder.html"

    def get_queryset(self):
        return Orders.objects.filter(status="order-placed")

class ProductListView(ListView):
    model = Products
    context_object_name = "products"
    template_name = "owner/product-list.html"

    # def get_queryset(self):
    #     return Products.objects.all()


class OrderDetailView(DetailView):
    model = Orders
    template_name = "owner/order-details.html"
    pk_url_kwarg = "id"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        form=OrderUpdateForm()
        context["form"]=form
        return context

    def post(self,request,args,*kw):
        order=self.get_object()
        print(self.get_object())
        form=OrderUpdateForm(request.POST)
        if form.is_valid():
            order.status=form.cleaned_data.get("status")
            order.expected_delivery_date=form.cleaned_data.get("expected_delivery_date")
            dt=form.cleaned_data.get("expected_delivery_date")
            order.save()
            send_mail(
                "order delivery update future store",
                f"your order will be delivered on {dt}",
                "vineeshm199812@gmail.com",
                ["vineeshm199811@gmail.com"]
            )
            print(form.cleaned_data)
            return redirect("dashboard")



from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect

from django.shortcuts import get_object_or_404
# from .models import Product

# @login_required
@require_http_methods(["GET", "POST"])
def adminpanel(request):
    # if not request.user.is_superuser:
    #     return redirect('product-list')

    products = Products.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm()

    return render(request, 'owner/admin_panel.html', {'products': products, 'form': form})

# def buy_product(request, pk):
#     product = get_object_or_404(Products, pk=pk)
#
#     if product.quantity > 0:
#         quantity_to_buy = 1  # You can modify this based on your requirements
#         if product.quantity >= quantity_to_buy:
#             product.quantity -= quantity_to_buy
#             product.save()
#     return redirect('product_detail', pk=pk)