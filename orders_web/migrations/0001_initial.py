from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ("applications_web", "0001_initial"),
        ("suppliers_web", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="PurchaseOrder",
            fields=[
                ("id", models.CharField(max_length=32, primary_key=True, serialize=False)),
                ("total", models.DecimalField(decimal_places=2, max_digits=14)),
                ("status", models.CharField(default="Оформлен", max_length=40)),
                ("application", models.OneToOneField(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="purchase_order", to="applications_web.application")),
                ("supplier", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="purchase_orders", to="suppliers_web.supplier")),
            ],
            options={"ordering": ["id"], "verbose_name": "Заказ поставщику",
                     "verbose_name_plural": "Заказы поставщикам"},
        ),
        migrations.AddConstraint(
            model_name="purchaseorder",
            constraint=models.CheckConstraint(
                condition=models.Q(("total__gte", 0)),
                name="purchase_order_total_gte_0",
            ),
        ),
    ]
