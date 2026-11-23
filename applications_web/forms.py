"""Формы заявок и состава закупки."""
from django import forms
from django.forms import inlineformset_factory

from common_forms import make_record_id
from .models import Application, ApplicationItem


class ApplicationFilterForm(forms.Form):
    q = forms.CharField(
        required=False, label="Поиск заявки",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    status = forms.ChoiceField(
        required=False, label="Статус",
        choices=(("", "Все статусы"),) + tuple(Application.Status.choices),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    exclude_status = forms.ChoiceField(
        required=False, label="Исключить статус",
        choices=(("", "Не исключать"),) + tuple(Application.Status.choices),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    sort = forms.ChoiceField(
        required=False, label="Сортировка",
        choices=(("id", "По ID"), ("purpose", "По назначению"), ("status", "По статусу")),
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ("purpose", "status")
        labels = {"purpose": "Назначение закупки", "status": "Статус"}
        widgets = {
            "purpose": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Цель закупки",
            }),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_purpose(self):
        purpose = self.cleaned_data["purpose"].strip()
        if len(purpose) < 5:
            raise forms.ValidationError("Опишите назначение закупки (не менее 5 символов).")
        return purpose

    def save(self, commit=True):
        application = super().save(commit=False)
        if not application.pk:
            application.id = make_record_id("APP")
        if commit:
            application.save()
            self.save_m2m()
        return application


class ApplicationItemForm(forms.ModelForm):
    quantity = forms.IntegerField(
        min_value=1, label="Количество",
        error_messages={"min_value": "Количество должно быть не меньше 1."},
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1}),
    )

    class Meta:
        model = ApplicationItem
        fields = ("product", "quantity")
        widgets = {
            "product": forms.Select(attrs={"class": "form-select"}),
        }


ApplicationItemFormSet = inlineformset_factory(
    Application,
    ApplicationItem,
    form=ApplicationItemForm,
    fields=("product", "quantity"),
    extra=1,
    can_delete=True,
    widgets={
        "product": forms.Select(attrs={"class": "form-select"}),
        "quantity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
    },
)
