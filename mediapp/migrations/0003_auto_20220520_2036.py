# Generated by Django 3.2.6 on 2022-05-20 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediapp', '0002_alter_customer_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='city',
            field=models.CharField(choices=[('Dhaka', 'Dhaka'), ('Khulna', 'Khulna'), ('Sylhet', 'Sylhet'), ('Rajshahi', 'Rajshahi'), ('Chittagong', 'Chittagong'), ('Rangpur', 'Rangpur'), ('Mymensingh', 'Mymensingh'), ('Comilla', 'Comilla'), ('Barishal', 'Barishal')], max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('C', 'Covid 19 Special'), ('D', 'Devices'), ('H', 'Herbal and Homeopathy'), ('BM', 'Baby & Mom care'), ('ND', 'Nutrition and drinks'), ('PC', 'Personal care'), ('OM', 'OTC Medicines'), ('PM', 'Prescription Medicines')], default='Sylhet', max_length=2),
        ),
    ]
