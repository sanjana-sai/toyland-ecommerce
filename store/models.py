from django.db import models

from  django.contrib.auth.models import User

from django.db.models.signals import post_save

# Create your models here.


class Category(models.Model):

    name=models.CharField(max_length=200,unique=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


    def __str__(self):

        return self.name


class Brand(models.Model):

    name=models.CharField(max_length=200,unique=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):

        return self.name
    
class AgeBetween(models.Model):

    age_group=models.CharField(max_length=200,unique=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):

        return self.age_group
    
class Size(models.Model):

    name=models.CharField(max_length=200,unique=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):

        return self.name
    
class Material(models.Model):

    name=models.CharField(max_length=200,unique=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):

        return self.name
    

class Colour(models.Model):

    name=models.CharField(max_length=200,unique=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):

        return self.name
    

class Product(models.Model):

    title=models.CharField(max_length=200)

    image=models.ImageField(upload_to="toyproductimages",null=True,default="default.jpg")

    description=models.TextField(null=True,blank=True)

    price=models.PositiveIntegerField()

    category_object=models.ForeignKey(Category,on_delete=models.CASCADE)

    brand_object=models.ForeignKey(Brand,on_delete=models.CASCADE)

    age_object=models.ManyToManyField(AgeBetween)

    size_object=models.ManyToManyField(Size)

    colour_object=models.ManyToManyField(Colour)

    material_object=models.ForeignKey(Material,on_delete=models.CASCADE)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def _str__(self):
        
        return self.title
    

class Basket(models.Model):

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):

        return self.owner.username
    
    @property
    def basketproduct_count(self):

        return self.cartitems.filter(is_order_placed=False).count()
    
    @property
    def cart_total(self):

        basket_items=self.cartitems.filter(is_order_placed=False)

        total_price=0

        if basket_items:
            for bi in basket_items:

                total_price+=bi.total_amount

        return total_price

        
    
class BasketItems(models.Model):

    basket_object=models.ForeignKey(Basket,on_delete=models.CASCADE,related_name="cartitems")

    product_object=models.ForeignKey(Product,on_delete=models.CASCADE)

    quantity=models.PositiveIntegerField(default=1)

    colour_object=models.ForeignKey(Colour,on_delete=models.CASCADE)

    agebetween_object=models.ForeignKey(AgeBetween,on_delete=models.CASCADE)

    size_object=models.ForeignKey(Size,on_delete=models.CASCADE)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    is_order_placed=models.BooleanField(default=False)

    @property
    def total_amount(self):      #custom method

       return self.product_object.price * self.quantity


class Order(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="myorders")

    basketitems_object=models.ManyToManyField(BasketItems)

    phone=models.CharField(max_length=200)

    email=models.EmailField()

    delivery_address=models.CharField(max_length=200)

    expected_delivery_date=models.DateField(null=True)

    pay_options=(
        ("cod","cod"),
        ("online","online"),
    )

    payment_method=models.CharField(max_length=200,choices=pay_options,default="cod")

    order_id=models.CharField(max_length=200,null=True)

    is_paid=models.BooleanField(default=False)

    order_status=(
        ("order_confirmed","order_confirmed"),
        ("dispatched","dispatched"),
        ("in_transit","in_transit"),
        ("delivered","delivered"),
        ("cancelled","cancelled"),

    )

    status=models.CharField(max_length=200,choices=order_status,default="order confirmed")
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    @property
    def order_total(self):


        basketitem_obj=self.basketitems_object.all()
 
        total=0

        if basketitem_obj:
           
            for bi in basketitem_obj:

                total+=bi.total_amount

        return total

def create_basket(sender,instance,created,**kwargs):  

    if created:

        Basket.objects.create(owner=instance)

post_save.connect(sender=User,receiver=create_basket)




