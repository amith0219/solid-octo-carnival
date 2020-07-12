from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.db.models import Avg,Count
    


class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(max_length=250)
    details = models.TextField(max_length=250, null=True, blank=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    

    def averagereview(self):
        reviews = Comment.objects.filter(product=self, status='New').aggregate(average=Avg('rate'))
        avg=0
        if reviews["average"] is not None:
            avg=float(reviews["average"])    
        return avg


    
    def countreview(self):
        reviews = Comment.objects.filter(product=self, status='New').aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

   

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return self.product.name

    
    def price(self):
        return self.product.price


    def total(self):
        total = self.quantity * self.product.price
        return total





class Order(models.Model):
    orderitems  = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ordered = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

    




    



class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    pincode = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.address
    
    
class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    rate = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    comment = models.CharField(max_length=250, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    