"""ORM-модели заявки и её товарных позиций."""
from decimal import Decimal

from django.db import models
from django.db.models import Count, F, Sum
from django.db.models.functions import Coalesce


class ApplicationQuerySet(models.QuerySet):
    """Переиспользуемые ORM-запросы для заявок."""

    def with_summary(self):
        """Добавляет количество позиций и сумму заявки, включая пустые заявки."""
        return self.annotate(
            item_count=Count("items", distinct=True),
            application_total=Coalesce(Sum("items__line_total"), Decimal("0.00")),
        )


class ApplicationManager(models.Manager.from_queryset(ApplicationQuerySet)):
    """Менеджер, предоставляющий методы ApplicationQuerySet."""


class Application(models.Model):
    class Status(models.TextChoices):
        DRAFT = "Черновик", "Черновик"
        APPROVED = "Согласована", "Согласована"
        REJECTED = "Отклонена", "Отклонена"

    id = models.CharField(
        primary_key=True, max_length=32, verbose_name="Идентификатор",
    )
    purpose = models.CharField(max_length=255, verbose_name="Назначение закупки")
    status = models.CharField(
        max_length=40, choices=Status.choices, default=Status.DRAFT, verbose_name="Статус",
    )
    objects = ApplicationManager()

    class Meta:
        ordering = ["id"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.id}: {self.purpose}"


class ApplicationItem(models.Model):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="items",
        verbose_name="Заявка",
    )
    product = models.ForeignKey(
        "products_web.Product", on_delete=models.PROTECT,
        related_name="application_items", verbose_name="Товар",
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    unit_price = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00"),
        verbose_name="Цена на момент добавления, руб.",
        help_text="Сохраняется как цена товара на момент добавления в заявку.",
    )
    line_total = models.GeneratedField(
        expression=F("unit_price") * F("quantity"),
        output_field=models.DecimalField(max_digits=14, decimal_places=2),
        db_persist=True,
        verbose_name="Сумма позиции, руб.",
    )

    class Meta:
        ordering = ["pk"]
        verbose_name = "Позиция заявки"
        verbose_name_plural = "Позиции заявок"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0), name="application_item_quantity_gt_0",
            ),
            models.CheckConstraint(
                condition=models.Q(unit_price__gte=0), name="application_item_unit_price_gte_0",
            ),
        ]

    def save(self, *args, **kwargs):
        if self._state.adding and self.unit_price == Decimal("0.00"):
            from products_web.models import Product

            self.unit_price = Product.objects.only("price").get(pk=self.product_id).price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} × {self.quantity}"
