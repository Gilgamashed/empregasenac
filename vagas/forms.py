from django import forms

from .models import Vagas


class VagasForm(forms.ModelForm):
    class Meta:
        model = Vagas
        fields = ['vaga', 'descricao', 'nivel', 'localidade', 'salario']


class CandidaturaForm(forms.Form):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()
    curriculo = forms.FileField()