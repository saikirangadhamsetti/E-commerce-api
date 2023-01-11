from _decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.contrib.auth.models import PermissionsMixin

from .utils import STATUS_CHOICES


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_instructor = True
        user.save(using=self._db)
        return user

    def create_customer(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_customer = True
        user.save(using=self._db)
        return user

    def create_seller(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_seller = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-id']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True



class CustomerAddress(models.Model):
    FirstName = models.CharField(max_length=17)
    LastName = models.CharField(max_length=17)
    phone = models.CharField(max_length=17, null=False)
    Email = models.EmailField(null=False,blank=False)
    CompanyName = models.CharField(max_length=100)
    Country = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    StreetAddress = models.TextField(max_length=200)
    zipcode = models.IntegerField(default=0)

    def __str__(self):
        return str(self.phone)


class Items(models.Model):
    seller = models.ForeignKey(get_user_model(), related_name='vendor', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    selling_price = models.FloatField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='Products/', blank=True, null=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)


class OrderPlaced(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE)
    product = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default=STATUS_CHOICES[0][0])
    Cost = models.FloatField()
    TotalCost = models.FloatField()




class productsUserReviewModel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="productsUserReviewModel_user")
    product = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="productsUserReviewModel_product")
    rating = models.DecimalField(max_digits=2, decimal_places=1,validators=[MinValueValidator(0), MaxValueValidator(5)])
    body = models.TextField()


