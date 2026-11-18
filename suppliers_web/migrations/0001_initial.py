from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Supplier",
            fields=[
                ("id", models.CharField(max_length=32, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=200)),
                ("contact", models.CharField(blank=True, default="", max_length=255)),
                ("rating", models.PositiveSmallIntegerField()),
            ],
            options={"ordering": ["-rating", "name"], "verbose_name": "Поставщик",
                     "verbose_name_plural": "Поставщики"},
        ),
        migrations.AddConstraint(
            model_name="supplier",
            constraint=models.CheckConstraint(
                condition=models.Q(("rating__gte", 1), ("rating__lte", 5), _connector="AND"),
                name="supplier_rating_1_to_5",
            ),
        ),
    ]
