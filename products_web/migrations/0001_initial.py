from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.CharField(max_length=32, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=200)),
                ("price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("description", models.TextField(blank=True, default="")),
            ],
            options={"ordering": ["name"], "verbose_name": "Товар",
                     "verbose_name_plural": "Товары"},
        ),
        migrations.AddConstraint(
            model_name="product",
            constraint=models.CheckConstraint(
                condition=models.Q(("price__gt", 0)), name="product_price_gt_0",
            ),
        ),
    ]
