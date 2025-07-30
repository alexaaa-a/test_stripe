from django.core.validators import MinValueValidator
from django.db import models


class Item(models.Model):
    """Модель товаров"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField(validators=[MinValueValidator(1)])
    currency = models.CharField(max_length=3, default='USD')

    def __str__(self):
        return self.name


class Order(models.Model):
    """Модель заказов"""
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey('Tax', on_delete=models.SET_NULL, null=True, blank=True)


class Discount(models.Model):
    """Модель скидок"""
    name = models.CharField(max_length=200)
    percent = models.PositiveIntegerField()
    stripe_coupon_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.percent}'


class Tax(models.Model):
    """Модель налогов"""
    name = models.CharField(max_length=200)
    percent = models.PositiveIntegerField()
    stripe_tax_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.percent}'