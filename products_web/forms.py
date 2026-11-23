"""Формы каталога товаров: фильтрация и CRUD."""
from decimal import Decimal

from django import forms

from .models import Product
from common_forms import make_record_id


class ProductFilterForm(forms.Form):
    q = forms.CharField(
        required=False, label="Поиск",
        widget=forms.TextInput(attrs={
            "class": "form-control", "placeholder": "Название или описание",
        }),
    )
    min_price = forms.DecimalField(
        required=False, min_value=Decimal("0.00"), max_digits=12, decimal_places=2,
        error_messages={"invalid": "Укажите корректную неотрицательную цену."},
        label="Минимальная цена",
        widget=forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.01"}),
    )
    sort = forms.ChoiceField(
        required=False, label="Сортировка",
        choices=(
            ("name", "По названию"), ("price", "Сначала дешевле"),
            ("-price", "Сначала дороже"),
        ),
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "price", "description", "image")
        labels = {
            "name": "Название товара",
            "price": "Цена, руб.",
            "description": "Описание",
            "image": "Изображение товара",
        }
        help_texts = {
            "price": "Укажите положительную цену в рублях.",
            "image": "Необязательное изображение товара (JPG, PNG или WebP).",
        }
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Например, Ноутбук",
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control", "min": "0.01", "step": "0.01",
            }),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control", "accept": "image/*",
            }),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Название должно содержать не менее двух символов.")
        return name

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("Цена товара должна быть больше нуля.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Размер изображения не должен превышать 5 МБ.")
        return image

    def save(self, commit=True):
        product = super().save(commit=False)
        if not product.pk:
            product.id = make_record_id("PRD")
        if commit:
            product.save()
            self.save_m2m()
        return product
