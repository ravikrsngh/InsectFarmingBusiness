from django.db import models

# Create your models here.


class Species(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Focus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class HomeCountry(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class InsectBusiness(models.Model):
    brand_name = models.CharField(max_length=50)
    parent_company = models.CharField(max_length=50,default="")
    home_country = models.ForeignKey(HomeCountry,on_delete=models.CASCADE, blank=True,null=True,related_name="home_country")
    updated = models.CharField(max_length=30, default="")
    active = models.CharField(max_length=10, default="")
    farm = models.CharField(max_length=10, default="")
    end_product = models.CharField(max_length=10)
    primary_focus = models.ForeignKey(Focus,on_delete=models.CASCADE, blank=True,null=True,related_name="primary_focus")
    secondary_focus = models.ForeignKey(Focus,on_delete=models.CASCADE, blank=True,null=True,related_name="secondary_focus")
    date_began = models.CharField(max_length=30)
    mailing_address = models.CharField(max_length=60)
    street_address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=60)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    contact_name = models.CharField(max_length=150)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=25)
    species = models.ManyToManyField(Species)

    def __str__(self):
        return self.brand_name
