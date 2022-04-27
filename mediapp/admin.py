from django.contrib import admin
from .models import(Customer,
                    Product,
                    Cart,
                    OrderPlaced, UploadPrescription, DoctorInfo, BkashPayment, NewTable)
# Register your models here.


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name',
                    'locality', 'city', 'zipcode', 'state']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price',
                    'description', 'brand', 'category', 'product_image']


@admin.register(Cart)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


@admin.register(OrderPlaced)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product',
                    'quantity', 'ordered_date', 'status']


@admin.register(UploadPrescription)
class UploadModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'prescription_image']


@admin.register(DoctorInfo)
class DoctorInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'specialist', 'chamber_address', 'city']


@admin.register(BkashPayment)
class BkashPaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'candidate_name', 'candidate_name', 'payment_amount']


@admin.register(NewTable)
class NewAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
