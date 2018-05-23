from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    datetime = forms.DateField(label="datetime", widget=forms.DateTimeInput(attrs={'type': 'date'}))