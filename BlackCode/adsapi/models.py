from django.db import models

# Create your models here


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=50)
    size = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-price']
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=['name', 'brand']),
            models.Index(fields=['price']),
            models.Index(fields=['category']),
        ]

