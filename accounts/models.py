from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from django.urls  import reverse
class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email')
        email = self.normalize_email(email)
        user = self.model(email=email,name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,name,password):
        """Create a new superuser with given details"""
        user = self.create_user(email,name,password)
        user.is_superuser =  True   #this is fetched from PermissionsMixin
        user.is_staff = True        #this is fetched from PermissionsMixin
        user.save(using=self._db)

        return user

class UserProfileInfo(AbstractBaseUser,PermissionsMixin):
    """Database model for user in the system"""
    email = models.EmailField(max_length=255, unique=True)  #no records with same email
    name = models.CharField(max_length=255)
    is_activated = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email
    
class Product(models.Model):
    name = models.CharField(max_length=255) 
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products')
    price = models.IntegerField() 

    def get_absolute_url(self):
        return reverse("accounts:product", kwargs={     # this will redirected to urls.py namespace = product
            "pk" : self.pk
        })
        
    def __str__(self):
        return self.name   

    def get_add_to_cart_url(self):
        return reverse("accounts:add-to-cart", kwargs={
            "pk" : self.pk
        })
        
@receiver(pre_delete, sender=Product)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.image.delete(False)

class OrderItem(models.Model):
    user = models.ForeignKey(UserProfileInfo,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"      
    def get_total_item_price(self):
        return self.quantity * self.product.price
        
class Order(models.Model):
    userprofileinfo = models.ForeignKey(UserProfileInfo,related_name='orders',on_delete=models.DO_NOTHING,)        
    products = models.ManyToManyField(OrderItem)   
    total_amount = models.IntegerField() 
    ordered = models.BooleanField(default=False)
    def __str__(self):
        return self.userprofileinfo.name   
    def cal_total_amount(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_total_item_price()
        return total  