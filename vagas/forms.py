from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Vagas


class VagasForm(forms.ModelForm):
    class Meta:
        model = Vagas
        fields = ['vaga', 'descricao', 'nivel', 'localidade', 'salario']
        widgets = {
                  'vaga' : forms.TextInput(attrs={'class': 'form-control'}),
                  'descricao': forms.Textarea(attrs={'class': 'form-control'}),
                  'nivel': forms.Select(attrs={'class': 'form-control'}),
                  'localidade':forms.TextInput(attrs={'class': 'form-control'}),
                  'salario': forms.NumberInput(attrs={'class':'form-control'})
        }
        labels = {
                  'vaga' : 'Titulo da Vaga',
                  'descricao': 'Descrição da Vaga',
                  'nivel': 'Nível',
                  'localidade': 'Localidade',
                  'salario': 'Salário'
        }


class CandidaturaForm(forms.Form):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()
    curriculo = forms.FileField()


class CandidatoSignUpForm(UserCreationForm):
    nome = forms.CharField(max_length=100)
    telefone = forms.CharField(max_length=20)
    cidade = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2' ]

class EmpresaSignUpForm(UserCreationForm):
    nome_empresa = forms.CharField(max_length=200)
    cnpj = forms.CharField(max_length=18)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']