from django.db import models

class RecyclableComponent(models.Model):
    name = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name

class RecyclableSpot(models.Model):
    name = models.CharField(max_length=500, null=True)
    address = models.CharField(max_length=500, null=True)
    latitude = models.DecimalField(max_digits=20, null=True, decimal_places=18)
    longitude = models.DecimalField(max_digits=20, null=True, decimal_places=18)
    recyclable_component = models.ForeignKey(RecyclableComponent, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name + " - " + self.address

class Component(models.Model):
    name = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)
    recyclable_component = models.ForeignKey(RecyclableComponent, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    barcode = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)
    component_set = models.ManyToManyField(Component, related_name="product_set", blank=True)

    def __str__(self):
        return self.name
