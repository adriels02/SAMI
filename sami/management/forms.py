from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email', 'class': 'form-control'
    }), label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Senha', 'class': 'form-control'
    }), label='Senha')

class RegisterForm(forms.Form):
    fullname = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nome completo', 'class': 'form-control', 'id': 'id_fullname'}),
        label='Nome completo'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control', 'id': 'id_email'}),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'class': 'form-control', 'id': 'id_password'}),
        label='Senha'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme sua senha', 'class': 'form-control', 'id': 'id_password_confirm'}),
        label='Confirme sua senha'
    )

