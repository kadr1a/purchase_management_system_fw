"""Django ORM-модель заказа поставщику."""
from django.db import models


class PurchaseOrderQuerySet(models.QuerySet):
    """Повторно используемые выборки заказов по статусу."""

    def ordered(self):
        return self.filter(status=self.model.Status.ORDERED)

    def cancelled(self):
        return self.filter(status=self.model.Status.CANCELLED)


class PurchaseOrderManager(models.Manager.from_queryset(PurchaseOrderQuerySet)):
    """Менеджер заказов с фильтрами по бизнес-статусам."""


class PurchaseOrder(models.Model):
    class Status(models.TextChoices):
        ORDERED = "Оформлен", "Оформлен"
        CANCELLED = "Отменён", "Отменён"

    id = models.CharField(primary_key=True, max_length=32, verbose_name="Идентификатор")
    application = models.OneToOneField(
        "applications_web.Application", on_delete=models.PROTECT,
        related_name="purchase_order", verbose_name="Заявка",
    )
    supplier = models.ForeignKey(
        "suppliers_web.Supplier", on_delete=models.PROTECT,
        related_name="purchase_orders", verbose_name="Поставщик",
    )
    total = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Сумма, руб.")
    status = models.CharField(
        max_length=40, choices=Status.choices, default=Status.ORDERED,
        verbose_name="Статус",
    )
    objects = PurchaseOrderManager()

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
        if self.status != self.Status.ORDERED:
            raise ValueError("Отменить можно только оформленный заказ.")
        self.status = self.Status.CANCELLED
        self.save(update_fields=["status"])
