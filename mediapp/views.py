from typing import Counter
from django import forms
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from . forms import CustomerRegistrationForm, CustomerProfileForm, DoctorInfoForm, UploadPrescriptionForm, AddProductForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from mediapp.models import Customer, UploadPrescription, DoctorInfo
import requests

# def home(request):
#  return render(request, 'app/home.html')


class ProductView(View):
    def get(self, request):
        myuser = request.user
        mainuser = Customer.objects.filter(user=myuser)
        if mainuser:
            covid = Product.objects.filter(category='C')
            devices = Product.objects.filter(category='D')[:4]
            herbal = Product.objects.filter(category='H')
            babymom = Product.objects.filter(category='BM')
            nudrinks = Product.objects.filter(category='ND')
            Persoal = Product.objects.filter(category='PC')
            otc = Product.objects.filter(category='OM')
            pm = Product.objects.filter(category='PM')
            fm = UploadPrescriptionForm()
            if request.user.is_authenticated:
                cart = Cart.objects.filter(user=request.user)
                return render(request, 'app/home.html', {'covid': covid, 'devices': devices, 'herbal': herbal, 'babymom': babymom, 'nudrinks': nudrinks, 'Persoal': Persoal, 'otc': otc, 'pm': pm, 'tcart': cart, "form": fm})
            else:
                return render(request, 'app/home.html', {'covid': covid, 'devices': devices, 'herbal': herbal, 'babymom': babymom, 'nudrinks': nudrinks, 'Persoal': Persoal, 'otc': otc, 'pm': pm, "form": fm})
        else:
            return redirect('profile')

    def post(self, request):
        covid = Product.objects.filter(category='C')
        devices = Product.objects.filter(category='D')[:4]
        herbal = Product.objects.filter(category='H')
        babymom = Product.objects.filter(category='BM')
        nudrinks = Product.objects.filter(category='ND')
        Persoal = Product.objects.filter(category='PC')
        otc = Product.objects.filter(category='OM')
        pm = Product.objects.filter(category='PM')
        fm = UploadPrescriptionForm()
        prescription_image = request.FILES['prescription_image']

        fm = UploadPrescription(
            newuser=request.user,  prescription_image=prescription_image)
        fm.save()
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)
            return render(request, 'app/home.html', {'covid': covid, 'devices': devices, 'herbal': herbal, 'babymom': babymom, 'nudrinks': nudrinks, 'Persoal': Persoal, 'otc': otc, 'pm': pm, 'tcart': cart, "form": fm})
        else:
            return render(request, 'app/home.html', {'covid': covid, 'devices': devices, 'herbal': herbal, 'babymom': babymom, 'nudrinks': nudrinks, 'Persoal': Persoal, 'otc': otc, 'pm': pm, "form": fm})

# def product_detail(request):
#     return render(request, 'app/productdetail.html')


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_cart = False
        if request.user.is_authenticated:

            item_already_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
            cart = Cart.objects.filter(user=request.user)
            return render(request, 'app/productdetail.html', {'product': product, 'item_already_cart': item_already_cart, 'tcart': cart})
        else:
            return render(request, 'app/productdetail.html', {'product': product, 'item_already_cart': item_already_cart})


@login_required
def add_to_cart(request):
    user = request.user

    product_id = request.GET.get('prod_id')

    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shiping_amount = 70.0
        total_amount = 0.0
        cart = Cart.objects.filter(user=request.user)
        empty_cart = "You Have No Product In Your Cart"
        buy_now = "Buy Now"
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + shiping_amount
        else:
            return render(request, 'app/addtocart.html', {'carts_empty': empty_cart, 'buy_now': buy_now, 'totalamount': total_amount, 'amount': amount, 'tcart': cart, })

        return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': total_amount, 'amount': amount, 'tcart': cart})


@login_required
def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shiping_amount = 70.0

        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount = amount + shiping_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': total_amount
        }

        return JsonResponse(data)


@login_required
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shiping_amount = 70.0

        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shiping_amount
        }

        return JsonResponse(data)


@login_required
def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shiping_amount = 70.0

        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {

            'amount': amount,
            'totalamount': amount + shiping_amount
        }

        return JsonResponse(data)


def buy_now(request, id):
    request.session['myproductid'] = id
    myproduct = Product.objects.get(id=id)
    price = myproduct.discounted_price
    total_price = price+70
    user = request.user
    add = Customer.objects.filter(user=user)
    return render(request, 'app/buynow.html', {'price': total_price, 'add': add})


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'app/address.html', {'add': add,  'active': 'btn-info', 'tcart': cart})
    else:
        return render(request, 'app/address.html', {'add': add,  'active': 'btn-info'})


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op, 'tcart': cart, })


def mobile(request, data=None):

    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung':
        mobiles = Product.objects.filter(category="M").filter(brand=data)
    elif data == "below":
        mobiles = Product.objects.filter(
            category="M").filter(discounted_price__lt=10000)
    elif data == "above":
        mobiles = Product.objects.filter(
            category="M").filter(discounted_price__gt=10000)

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'app/mobile.html', {'mobiles': mobiles, 'tcart': cart})

    return render(request, 'app/mobile.html', {'mobiles': mobiles})


def laptob(request, data=None):

    if data == None:
        laptob = Product.objects.filter(category='L')
    elif data == 'HP' or data == 'MAC' or data == "Lenevo":
        laptob = Product.objects.filter(category="L").filter(brand=data)
    elif data == "below":
        laptob = Product.objects.filter(
            category="L").filter(discounted_price__lt=40000)
    elif data == "above":
        laptob = Product.objects.filter(
            category="L").filter(discounted_price__gt=40000)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'app/laptob.html', {'laptob': laptob, 'tcart': cart})
    return render(request, 'app/laptob.html', {'laptob': laptob})


def covid(request):

    covid = Product.objects.filter(category='C')

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'app/covid.html', {'covid': covid, 'tcart': cart})
    return render(request, 'app/covid.html', {'covid': covid})


def devices(request):

    devices = Product.objects.filter(category='D')
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'app/devices.html', {'devices': devices, 'tcart': cart})
    return render(request, 'app/devices.html', {'devices': devices})


def Herbal(request):

    Herbal = Product.objects.filter(category='H')

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'app/Herbal.html', {'Herbal': Herbal, 'tcart': cart})
    return render(request, 'app/Herbal.html', {'Herbal': Herbal})


def BabyMom(request):

    BabyMom = Product.objects.filter(category='BM')

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'app/BabyMom.html', {'BabyMom': BabyMom, 'tcart': cart})
    return render(request, 'app/BabyMom.html', {'BabyMom': BabyMom})


def Nutrition(request):

    Nutrition = Product.objects.filter(category='ND')

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'app/Nutrition.html', {'Nutrition': Nutrition, 'tcart': cart})
    return render(request, 'app/Nutrition.html', {'Nutrition': Nutrition})


def PersonalCare(request, data=None):

    devices = Product.objects.filter(category='D')

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'app/devices.html', {'devices': devices, 'tcart': cart})
    return render(request, 'app/devices.html', {'devices': devices})


def OTC(request):

    devices = Product.objects.filter(category='D')

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'app/devices.html', {'devices': devices, 'tcart': cart})
    return render(request, 'app/devices.html', {'devices': devices})


def Prescription(request):

    devices = Product.objects.filter(category='D')

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'app/devices.html', {'devices': devices, 'tcart': cart})
    return render(request, 'app/devices.html', {'devices': devices})


# def login(request):
#     return render(request, 'app/login.html')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()

        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Congratulations!! Registered Successfully')

        return render(request, 'app/customerregistration.html', {'form': form})


@login_required
def checkout(request):
    try:
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0.0
        shiping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
            total_amount += amount + shiping_amount

        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)
            return render(request, 'app/checkout.html', {'add': add, 'total_amount': total_amount, 'cart_items': cart_items, 'tcart': cart})

        return render(request, 'app/checkout.html', {'add': add, 'total_amount': total_amount, 'cart_items': cart_items})
    except:
        messages.success(request, "Please Add Your Profile For Place Order")
        return redirect('profile')


@login_required
def payment_done(request):
    try:
        user = request.user
        custid = request.GET.get('custid')
        customer = Customer.objects.get(id=custid)
        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user, customer=customer,
                        product=c.product, quantity=c.quantity).save()
            c.delete()

        return redirect('orders')
    except:
        messages.success(request, "Please Add Your Profile For Place Order")
        return redirect('profile')


@login_required
def buy_payment_done(request):
    try:
        n = request.session.get('myproductid')
        user = request.user
        custid = request.GET.get('custid')
        customer = Customer.objects.get(id=custid)
        product = Product.objects.get(id=n)

        OrderPlaced(user=user, customer=customer,
                    product=product, quantity=1).save()

        return redirect('orders')
    except:
        messages.success(request, "Please Add Your Profile For Place Order")
        return redirect('profile')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):

        form = CustomerProfileForm()
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)
            return render(request, 'app/profile.html', {'form': form, 'active': 'btn-info', 'tcart': cart})
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-info'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality,
                           city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(
                request, 'Congratulations Profile Updated Successfully')
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)
            return render(request, 'app/profile.html', {'form': form, 'active': 'btn-info', 'tcart': cart})
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-info'})


class PasswordChangeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)
            return render(request, 'app/passwordchange.html', {'tcart': cart})
        else:
            return render(request, 'app/passwordchange.html')


def searchhresult(request):
    search = request.POST.get('search')

    allpro = Product.objects.filter(
        title=search) or Product.objects.filter(brand=search)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'app/search.html', {'product': allpro, 'tcart': cart})
    return render(request, 'app/search.html', {'product': allpro})


def doctor(request):
    doctor_info = DoctorInfo.objects.all()
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'app/doctor.html', {'tcart': cart, 'doctor_info': doctor_info})
    return render(request, 'app/doctor.html', {'doctor_info': doctor_info})


def doctor_details(request, id):
    doctor_info = DoctorInfo.objects.get(id=id)

    return render(request, 'app/doctor_details.html', {'doctorallinfo': doctor_info})


def covidinformation(request):
    data = True
    result = None
    globalSummary = None
    countries = None
    while(data):
        try:
            result = requests.get('https://api.covid19api.com/summary')
            globalSummary = result.json()['Global']
            countries = result.json()['Countries']
            data = False
        except:
            data = True

    return render(request, 'app/covidinformation.html', {'globalSummary': globalSummary, "countries": countries})


class DoctorADD(View):
    def get(self, request):
        fm = DoctorInfoForm()
        return render(request, 'app/doctoradd.html', {'form': fm})

    def post(self, request):
        fm = DoctorInfoForm(request.POST, request.FILES)
        if fm.is_valid():
            fm.save()
        return render(request, 'app/doctoradd.html', {'form': fm})


class Addproduct(View):
    def get(self, request):
        fm = AddProductForm()
        return render(request, 'app/productadd.html', {'form': fm})

    def post(self, request):
        fm = AddProductForm(request.POST, request.FILES)
        if fm.is_valid():
            fm.save()
        return render(request, 'app/productadd.html', {'form': fm})
