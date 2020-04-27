from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CASCADE

from shop.choices import city_choices


class Contact(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=250)
    email = models.EmailField()
    subject = models.CharField(max_length=250, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.id, self.name, self.email, self.subject, self.message


class Pharmacy(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=CASCADE)

    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='pharmacy_pics', blank="x.img")
    x = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    y = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    slot4hMinWeek = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(42)])  # 24/4 * 7
    location = models.CharField(max_length=250, choices=city_choices)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "[" + self.id.__str__() + "] " + self.name

    def __unicode__(self):
        return self.id, self.owner, self.name

    def getSlot4hMinWeek(self):
        return self.slot4hMinWeek

    def getId(self):
        return self.id

    class Meta:
        verbose_name_plural = "Pharmacies"


class Category(models.Model):
    id = models.AutoField(primary_key=True)

    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.id, self.name, self.description

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=CASCADE)

    slug = AutoSlugField(populate_from='id')
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='products')
    description = models.TextField(blank=True, default="Description field")
    brand = models.CharField(max_length=250)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.id, self.name, self.description


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    review = models.CharField(max_length=1000, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.__str__()

    def __unicode__(self):
        return self.id, self.review


class Buyer(models.Model):
    id = models.AutoField(primary_key=True)

    full_name = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=250, choices=city_choices)
    address = models.CharField(max_length=250, default="via Vittoria 10")
    product = models.ManyToManyField(Product)

    def __str__(self):
        return self.full_name

    def __unicode__(self):
        return self.id, self.full_name, self.phone
