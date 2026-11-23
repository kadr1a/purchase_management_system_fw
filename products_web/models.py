"""Django ORM-модель товара."""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


_CYRILLIC_TRANSLITERATION = str.maketrans({
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e",
    "ё": "yo", "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k",
    "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r",
    "с": "s", "т": "t", "у": "u", "ф": "f", "х": "kh", "ц": "ts",
    "ч": "ch", "ш": "sh", "щ": "shch", "ъ": "", "ы": "y", "ь": "",
    "э": "e", "ю": "yu", "я": "ya",
})


def make_product_slug(value):
    """Преобразует русское название товара в URL-slug латиницей."""
    transliterated = value.lower().translate(_CYRILLIC_TRANSLITERATION)
    return slugify(transliterated) or "product"


class Product(models.Model):
    id = models.CharField(
        primary_key=True, max_length=32, verbose_name="Идентификатор",
    )
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(
        max_length=220, unique=True, blank=True, editable=False,
        verbose_name="Адрес страницы",
    )
    price = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Цена, руб.",
    )
    description = models.TextField(
        blank=True, default="", verbose_name="Описание",
    )
    image = models.ImageField(
        upload_to="products/", blank=True, null=True, verbose_name="Изображение",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gt=0), name="product_price_gt_0",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = make_product_slug(self.name)
            candidate = base_slug
            suffix = 2
            while Product.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = candidate
            update_fields = kwargs.get("update_fields")
            if update_fields is not None:
                kwargs["update_fields"] = set(update_fields) | {"slug"}
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:detail-by-slug", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"
