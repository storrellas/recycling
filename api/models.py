from django.db import models

class RecyclableProduct(models.Model):
    name = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    barcode = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name

class RecyclableSpot(models.Model):
    name = models.CharField(max_length=500, null=True)
    address = models.CharField(max_length=500, null=True)
    latitude = models.DecimalField(max_digits=5, null=True, decimal_places=2)
    longitude = models.DecimalField(max_digits=5, null=True, decimal_places=2)
    recyclable_product = models.ForeignKey(RecyclableProduct, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Component(models.Model):
    name = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)
    product_set = models.ManyToManyField(Product, related_name="components_set", blank=True)
    recyclable_product = models.ForeignKey(RecyclableProduct, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
