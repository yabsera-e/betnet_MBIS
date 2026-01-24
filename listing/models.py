from django.db import models
from users.models import CustomUser


class City(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        db_table = 'cities'

    def __str__(self):
        return self.name

class SubCity(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        db_table = 'subcities'
    
    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'amenities'

class Listing(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='listings')
    title = models.CharField( max_length=50)
    desc = models.TextField(max_length=400,null=True, blank=True)
    price = models.DecimalField( max_digits=10, decimal_places=2)
    rooms = models.IntegerField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    square_metre = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    sub_city = models.ForeignKey(SubCity, on_delete=models.SET_NULL, null=True, blank=True)
    area = models.CharField( max_length=100, null=True, blank=True)
    phone_number1 = models.CharField(max_length=20)
    phone_number2 = models.CharField(max_length=20, null=True, blank=True)
    status = models.BooleanField(default=True)
    admin_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    amenities = models.ManyToManyField(Amenity, blank=True, related_name='listings')

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'listings'

class ListingMedia(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='medias')
    file_path = models.TextField()
    file_name = models.TextField(null=True, blank=True)
    media_type = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'listing_medias'

