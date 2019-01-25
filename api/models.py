from django.db import models

class RecyclableMaterial(models.Model):
    name = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name

class RecyclableSpot(models.Model):
    name = models.CharField(max_length=500, null=True)
    address = models.CharField(max_length=500, null=True)
    latitude = models.DecimalField(max_digits=20, null=True, decimal_places=18)
    longitude = models.DecimalField(max_digits=20, null=True, decimal_places=18)
    recyclable_material = models.ForeignKey(RecyclableMaterial, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name + " - " + self.address

class Material(models.Model):
    name = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)
    recyclable_material = models.ForeignKey(RecyclableMaterial, on_delete=models.SET_NULL, null=True)

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
        return self.name

class RecyclableHistory(models.Model):
    UID = models.CharField(max_length=500, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.barcode + " - " + self.created_at


class New(models.Model):
    title = models.CharField(max_length=500, null=True)
    content = models.CharField(max_length=500, null=True)
    media = models.URLField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
