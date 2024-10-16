from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class User(models.Model):
    userID=models.AutoField(primary_key=True)
    name=models.TextField()
    email=models.EmailField(unique=True)
    phone=models.TextField()
    password=models.TextField()
    def clean(self):
        if Staff.objects.filter(email=self.email).exists():
            raise ValidationError(f"Email {self.email} is already registered as Staff.")

class Cafe(models.Model):
    cafeID=models.AutoField(primary_key=True)
    name=models.TextField()

class Menu(models.Model):
    menuID=models.AutoField(primary_key=True)
    name=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    cafeID=models.ForeignKey(Cafe, on_delete=models.CASCADE)

class Staff(models.Model):
    staffID=models.AutoField(primary_key=True)
    email=models.EmailField(unique=True)
    password=models.TextField()
    name=models.TextField()
    phone=models.TextField()
    cafeID=models.ForeignKey(Cafe, on_delete=models.CASCADE)
    def clean(self):
        if User.objects.filter(email=self.email).exists():
            raise ValidationError(f"Email {self.email} is already registered as User.")

class Order(models.Model):
    ORDER_STATUS = [
        (0, 'Order Received'),
        (1, 'Preparing'),
        (2, 'Ready to Pick Up'),
        (3, 'Picked Up'),
    ]
    PAYMENT = [
        (0, 'Not Pay'),
        (1, 'Paid')
    ]
    
    orderID = models.AutoField(primary_key=True)
    menuID = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cafeID = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2,editable=False)
    status = models.IntegerField(choices=ORDER_STATUS, default=0)
    pay=models.IntegerField(choices=PAYMENT,default=0)
    def save(self, *args, **kwargs):
        # Get the price from the related Menu object
        self.total_price = self.menuID.price * self.quantity
        super(Order, self).save(*args, **kwargs)  # Call the "real" save() method

class Admin(models.Model):
    adminID=models.AutoField(primary_key=True)
    name=models.TextField()
    phone=models.TextField()
    email=models.EmailField()
    password=models.TextField()
    def clean(self):
        if User.objects.filter(email=self.email).exists():
            raise ValidationError(f"Email {self.email} is already registered as User.")
        if Staff.objects.filter(email=self.email).exists():
            raise ValidationError(f"Email {self.email} is already registered as Staff.")

