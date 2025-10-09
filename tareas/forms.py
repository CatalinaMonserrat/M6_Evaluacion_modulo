from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TareaForm(forms.Form):
    titulo = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ["username", "password1", "password2"]:
            self.fields[f].widget.attrs.update({'class': 'form-control'}) 