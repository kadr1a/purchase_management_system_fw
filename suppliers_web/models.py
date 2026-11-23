"""Django ORM-модель поставщика."""
from django.db import models


class Supplier(models.Model):
    id = models.CharField(primary_key=True, max_length=32, verbose_name="Идентификатор")
    name = models.CharField(max_length=200, verbose_name="Название поставщика")
    contact = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Контактные данные",
    )
    rating = models.PositiveSmallIntegerField(verbose_name="Рейтинг")

    class Meta:
        ordering = ["-rating", "name"]
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name="supplier_rating_1_to_5",
            ),
        ]

    def __str__(self):
        return self.name
