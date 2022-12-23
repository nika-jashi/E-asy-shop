from django.db import models
from apps.accounts.models import CustomAccount


class Product(models.Model):
    product_title = models.CharField(max_length=256)
    product_description = models.TextField(max_length=1024)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    seller = models.ForeignKey(to=CustomAccount, on_delete=models.CASCADE)
    date_listed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_title


class MainCategory(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=128)
    main_category_name = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_category_name
