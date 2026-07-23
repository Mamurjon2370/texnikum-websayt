from django import forms
from .models import Application, ContactMessage


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["full_name", "birth_date", "phone", "email", "program", "prev_school", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Familiya Ism Sharif"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+998 __ ___ __ __"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "email@example.com"}),
            "program": forms.Select(attrs={"class": "form-select"}),
            "prev_school": forms.TextInput(attrs={"class": "form-control", "placeholder": "Maktab / muassasa"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ismingiz"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "E-mail"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Telefon"}),
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "Mavzu"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Xabaringiz"}),
        }
