"""Формы фильтрации и оформления заказа поставщику."""
from django import forms

from common_forms import make_record_id
from applications_web.models import Application
from .models import PurchaseOrder


class OrderFilterForm(forms.Form):
    q = forms.CharField(
        required=False, label="Поиск",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    status = forms.ChoiceField(
        required=False, label="Статус",
        choices=(("", "Все статусы"),) + tuple(PurchaseOrder.Status.choices),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    sort = forms.ChoiceField(
        required=False, label="Сортировка",
        choices=(("id", "По номеру"), ("total", "По сумме"), ("supplier", "По поставщику"),
                 ("application", "По заявке")),
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ("application", "supplier")
        labels = {"application": "Заявка", "supplier": "Поставщик"}
        widgets = {
            "application": forms.Select(attrs={"class": "form-select"}),
            "supplier": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["application"].queryset = (
            Application.objects.filter(purchase_order__isnull=True).order_by("id")
        )

    def save(self, commit=True):
        order = super().save(commit=False)
        if not order.pk:
            order.id = make_record_id("ORD")
        if commit:
            order.save()
            self.save_m2m()
        return order
