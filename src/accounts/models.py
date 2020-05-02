from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    """Model definition for Customer."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name =  models.CharField(max_length = 255, null = True)
    phone = models.CharField(max_length = 14, null = True)
    email = models.EmailField(max_length= 255, null = True)
    profile_image = models.ImageField(null=True, blank=True, default='default_profile.png')
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Customer."""

        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        """Unicode representation of Customer."""
        return self.email
    
class Tag(models.Model):
    """Model definition for Tag."""

    name = models.CharField(max_length= 255, null = True)

    class Meta:
        """Meta definition for Tag."""

        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        """Unicode representation of Tag."""
        return self.name

class Product(models.Model):
    """Model definition for Product."""
    CATEGORY = (('INDOOR', 'IN-DOOR'),
                ('OUTDOOR','OUT DOOR'))

    name = models.CharField(max_length = 255, null = True)
    price = models.FloatField(null= True)
    category = models.CharField(max_length = 255, null = True, choices = CATEGORY)
    description = models.CharField(max_length = 255, null = True)
    create_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag) # Many to many field 

    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """Unicode representation of Product."""
        return self.name
    

    
class Order(models.Model):
    """Model definition for Order."""
    STATUS = (
        ('PENDING', 'PENDING'),
        ('OUT_FOR_DEVLIVERY', 'OUT FOR DELEVERY'),
        ('DELIVERED', 'DELIVERED')
    )
    customer = models.ForeignKey(Customer, null = True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null = True, on_delete=models.SET_NULL)
    status = models.CharField(choices=STATUS, max_length = 200, null = True)
    create_date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, null=True)

    class Meta:
        """Meta definition for Order."""

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        """Unicode representation of Order."""
        return self.product.name


