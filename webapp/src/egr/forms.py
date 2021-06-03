from django import forms

class EgrDateSelectForm(forms.Form):
    date=forms.DateField(label="На дату", required=True)