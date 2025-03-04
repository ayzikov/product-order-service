# installed
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class Provider(models.Model):
    """ Поставщик """
    name = models.CharField(max_length=200, verbose_name="наименование организации")
    country = models.CharField(max_length=200, verbose_name="страна")
    town = models.CharField(max_length=200, verbose_name="город")
    street = models.CharField(max_length=200, verbose_name="улица")
    building = models.IntegerField(verbose_name="здание")


class Category(MPTTModel):
    """ Категория товара """
    name = models.CharField(max_length=200, verbose_name="название")
    parent = TreeForeignKey(
        to='self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='родительская категория'
    )

    class MPTTMeta:
        """ Сортировка по вложенности """
        order_insertion_by = ('name',)


class Product(models.Model):
    """ Товар """
    name = models.CharField(max_length=200, verbose_name="название")
    price = models.IntegerField(verbose_name="цена")
    provider = models.ForeignKey(to=Provider, on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)


class RemainingStock(models.Model):
    """ Остаток товара на складе """
    quantity = models.IntegerField(default=0, verbose_name="количество")
    product = models.OneToOneField(to=Product, on_delete=models.CASCADE)


class Buyer(AbstractUser):
    """ Покупатель """
    first_name = models.CharField(max_length=150, verbose_name="имя")
    last_name = models.CharField(max_length=150, verbose_name="фамилия")
    age = models.IntegerField(verbose_name="возраст")
    email = models.EmailField(validators=[EmailValidator],unique=True, null=False)
    is_verified = models.BooleanField(default=False, verbose_name="подтверждение по email")

    # в поле username нужно вводить email, а не username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Order(models.Model):
    """ Заказ """
    datetime = models.DateTimeField(default=timezone.now, verbose_name="дата и время заказа")
    buyer = models.ForeignKey(to=Buyer, on_delete=models.CASCADE)


class ProductOrder(models.Model):
    """ Товар в заказе """
    quantity = models.IntegerField(verbose_name="количество")
    purchase_price = models.IntegerField(verbose_name="закупочная цена")
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
