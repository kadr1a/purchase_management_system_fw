"""Формы поиска и редактирования поставщиков."""
from django import forms

from common_forms import make_record_id
from .models import Supplier


class SupplierFilterForm(forms.Form):
    q = forms.CharField(
        required=False, label="Поиск",
        widget=forms.TextInput(attrs={
            "class": "form-control", "placeholder": "Название или контакт",
        }),
    )
    exact_name = forms.CharField(
        required=False, label="Точное название",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    min_rating = forms.IntegerField(
        required=False, min_value=1, max_value=5,
        error_messages={
            "invalid": "Рейтинг должен быть целым числом от 1 до 5.",
            "min_value": "Рейтинг должен быть от 1 до 5.",
            "max_value": "Рейтинг должен быть от 1 до 5.",
        },
        label="Минимальный рейтинг",
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
    )


class SupplierForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1, max_value=5, label="Рейтинг",
        error_messages={
            "min_value": "Рейтинг должен быть от 1 до 5.",
            "max_value": "Рейтинг должен быть от 1 до 5.",
            "invalid": "Введите целое число от 1 до 5.",
        },
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
    )

    class Meta:
        model = Supplier
        fields = ("name", "contact", "rating")
        labels = {
            "name": "Название поставщика",
            "contact": "Контактные данные",
            "rating": "Рейтинг",
        }
        help_texts = {"rating": "Целое число от 1 до 5."}
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "contact": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Телефон или e-mail",
            }),
        }

    def clean_name(self):
        value = self.cleaned_data["name"].strip()
        if len(value) < 2:
            raise forms.ValidationError("Название поставщика слишком короткое.")
        return value

    def save(self, commit=True):
        supplier = super().save(commit=False)
        if not supplier.pk:
            supplier.id = make_record_id("SUP")
        if commit:
            supplier.save()
            self.save_m2m()
        return supplier
