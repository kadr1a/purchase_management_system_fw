"""Django ORM-модель товара."""
from django.db import models


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gt=0), name="product_price_gt_0",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"
