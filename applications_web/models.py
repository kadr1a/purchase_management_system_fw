"""ORM-модели заявки и её товарных позиций."""
from django.db import models


class Application(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    purpose = models.CharField(max_length=255)
    status = models.CharField(max_length=40, default="Черновик")

    class Meta:
        ordering = ["id"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.id}: {self.purpose}"


class ApplicationItem(models.Model):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="items",
    )
    product = models.ForeignKey(
        "products_web.Product", on_delete=models.PROTECT,
        related_name="application_items",
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        ordering = ["pk"]
        verbose_name = "Позиция заявки"
        verbose_name_plural = "Позиции заявок"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0), name="application_item_quantity_gt_0",
            ),
        ]

    def __str__(self):
        return f"{self.product} × {self.quantity}"
