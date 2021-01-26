from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        user = self.model(email=email, password=password)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        return self.get(email=email_)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Here we are subclassing the Django AbstractBaseUser, which comes with only
    3 fields:
    1 - password
    2 - last_login
    3 - is_active
    Note than all fields would be required unless specified otherwise, with
    `required=False` in the parentheses.
    The PermissionsMixin is a model that helps you implement permission settings
    as-is or modified to your requirements.
    More info: https://goo.gl/YNL2ax
    """

    name = models.CharField(max_length=30, default='', null=True,
                            verbose_name=u"Name of User")
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=255)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'email'

    objects = CustomAccountManager()

    def __str__(self):
        return "{} - {}".format(self.name, self.email)

    def get_username(self):
        return self.email

    def username(self):
        return self.email

    def get_short_name(self):
        return self.name

    def natural_key(self):
        return self.email


class BakeryIngredient(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    is_available = models.BooleanField(default=False)
    available_quantity = models.FloatField(null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BakeryItem(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    available_quantity = models.IntegerField(default=0)
    cost_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BakeryItemIngredient(models.Model):
    bakery_item = models.ForeignKey("bakery.BakeryItem",
                                    on_delete=models.CASCADE)
    bakery_ingredient = models.ForeignKey("bakery.BakeryIngredient",
                                          on_delete=models.CASCADE)
    quantity_percent = models.FloatField(blank=False, null=False)

    def __str__(self):
        return self.bakery_item.name


class Order(models.Model):
    bakery_item = models.ForeignKey("bakery.BakeryItem",
                                    on_delete=models.CASCADE)
    user = models.ForeignKey("bakery.User", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bakery_item.name
