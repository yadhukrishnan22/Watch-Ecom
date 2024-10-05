from django.db import models

from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save

from django.db.models import Sum

from django.core.validators import MinValueValidator, MaxValueValidator



class UserProfile(models.Model):

    bio=models.CharField(max_length=260,null=True)

    profile_pic=models.ImageField(upload_to="profile_pictures",default="/profile_pictures/default.png")

    user_object=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


    def __str__(self) -> str:

        return self.user_object.username
    


class Brand(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):

        return self.name

    


class IdealFor(models.Model):

    for_name = models.CharField(max_length=100)

    def __str__(self):

        return self.for_name


class Type(models.Model):

    type_name = models.CharField(max_length=100)

    def __str__(self):

        return self.type_name



class Product(models.Model):

    title = models.CharField(max_length=100)

    base_price = models.PositiveIntegerField()

    description = models.CharField(max_length=300)

    image = models.ImageField(upload_to='product_images')

    mfg_date = models.DateField()

    brand_obj = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand')

    type_obj = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='type')

    for_obj = models.ForeignKey(IdealFor, on_delete=models.CASCADE, related_name='idealfor')

    is_active = models.BooleanField(default=False)


    def __str__(self):

        return self.title




class Color(models.Model):

    color_name = models.CharField(max_length=100)

    def __str__(self):

        return self.color_name



class ProductVarient(models.Model):

    product_obj = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')

    color_obj = models.ManyToManyField(Color, related_name='color')

    varient_image = models.ImageField(upload_to='varient_images', null=True)

    price = models.PositiveIntegerField()

        



class Cart(models.Model):

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="basket")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


    @property
    def cartlist_total(self):

        return self.basket_items.filter(is_order_placed = False).values('product_varient_object__price').aggregate(total = Sum('product_varient_object__price')).get('total')



class CartItems(models.Model):

    cart_object=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="basket_items")

    product_varient_object = models.ForeignKey(ProductVarient, on_delete=models.CASCADE)

    is_order_placed=models.BooleanField(default=False)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)
    
    


class OrderSummary(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")

    product_varient_object=models.ManyToManyField(ProductVarient)

    phone = models.CharField(max_length= 10)

    email = models.EmailField(max_length= 200)

    pin = models.PositiveIntegerField()

    delivery_address = models.CharField(max_length=300)

    order_id=models.CharField(max_length=200,null=True)

    is_paid=models.BooleanField(default=False)
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    total = models.FloatField(null = True)

    payment_choices = (
        ("Upi", "Upi"),
        ('Cash', "Cash")
    )

    payment_method = models.CharField(max_length=100, choices=payment_choices, default='Upi')


class Reviews(models.Model):

    product_object = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='project_reviews')

    user_object = models.ForeignKey(User, on_delete=models.CASCADE)

    comment = models.TextField()

    rating = models.PositiveBigIntegerField(default=1, validators=(MinValueValidator(1), MaxValueValidator(5)))

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)



def create_profile(sender, instance, created, *args, **kwargs):

    if created:

        UserProfile.objects.create(user_object = instance)

post_save.connect(sender = User, receiver= create_profile)


def create_basket(sender, instance, created, *args, **kwargs):

    if created:

        Cart.objects.create(owner = instance)
        
post_save.connect(sender= User, receiver= create_basket)

    

    

