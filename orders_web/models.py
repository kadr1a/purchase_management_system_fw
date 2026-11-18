"""Django ORM-модель заказа поставщику."""
from django.db import models


class PurchaseOrder(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    application = models.OneToOneField(
        "applications_web.Application", on_delete=models.PROTECT,
        related_name="purchase_order",
    )
    supplier = models.ForeignKey(
        "suppliers_web.Supplier", on_delete=models.PROTECT,
        related_name="purchase_orders",
    )
    total = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=40, default="Оформлен")

    class Meta:
        ordering = ["id"]
        verbose_name = "Заказ поставщику"
        verbose_name_plural = "Заказы поставщикам"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(total__gte=0), name="purchase_order_total_gte_0",
            ),
        ]

    def __str__(self):
        return f"{self.id}: {self.supplier} — {self.total} руб."

    def cancel(self):
        if self.status != "Оформлен":
            raise ValueError("Отменить можно только оформленный заказ.")
        self.status = "Отменён"
        self.save(update_fields=["status"])
