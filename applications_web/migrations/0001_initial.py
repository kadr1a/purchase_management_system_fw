from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ("products_web", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                ("id", models.CharField(max_length=32, primary_key=True, serialize=False)),
                ("purpose", models.CharField(max_length=255)),
                ("status", models.CharField(default="Черновик", max_length=40)),
            ],
            options={"ordering": ["id"], "verbose_name": "Заявка",
                     "verbose_name_plural": "Заявки"},
        ),
        migrations.CreateModel(
            name="ApplicationItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField()),
                ("application", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="items", to="applications_web.application")),
                ("product", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="application_items", to="products_web.product")),
            ],
            options={"ordering": ["pk"], "verbose_name": "Позиция заявки",
                     "verbose_name_plural": "Позиции заявок"},
        ),
        migrations.AddConstraint(
            model_name="applicationitem",
            constraint=models.CheckConstraint(
                condition=models.Q(("quantity__gt", 0)),
                name="application_item_quantity_gt_0")),
    ]
