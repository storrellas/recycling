from django.db import models
from django.contrib.auth import get_user_model

class RecyclingMaterial(models.Model):
    name = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)
    media = models.URLField(max_length=500, null=True)

    def __str__(self):
        return self.name

class RecyclingSpot(models.Model):
    name = models.CharField(max_length=500, null=True)
    address = models.CharField(max_length=500, null=True)
    latitude = models.DecimalField(max_digits=20, null=True, decimal_places=18)
    longitude = models.DecimalField(max_digits=20, null=True, decimal_places=18)
    recycling_material = models.ForeignKey(RecyclingMaterial, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name + " - " + self.address

class Material(models.Model):
    name = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)
    recycling_material = models.ForeignKey(RecyclingMaterial, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    barcode = models.CharField(max_length=500, primary_key=True)
    name = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)
    latitude = models.DecimalField(max_digits=20, null=True, decimal_places=18)
    longitude = models.DecimalField(max_digits=20, null=True, decimal_places=18)
    media = models.URLField(max_length=500, null=True)
    material_set = models.ManyToManyField(Material, related_name="product_set", blank=True)

    def __str__(self):
        return self.barcode + " - " + self.name

class RecyclingHistory(models.Model):
    UID = models.CharField(max_length=500, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.barcode + " - " + self.product.name


class New(models.Model):
    title = models.CharField(max_length=500, null=True)
    content = models.CharField(max_length=500, null=True)
    media = models.URLField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
