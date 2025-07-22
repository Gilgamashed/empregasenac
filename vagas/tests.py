import pytest
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from vagas.models import Candidato, Empresa, Vagas


class CandidaturaAccessTest(TestCase):
    def setUp(self):
        self.client= Client()

        #usuario candidato
        self.candidato_user = User.objects.create_user(username='candidatoTest1', password='senha@123')
        self.candidato = Candidato.objects.create(
            user=self.candidato_user,
            nome='Caius',
            telefone='21 123456789',
            cidade='Rio de Janeiro'
        )

        #usuario empresa
        self.empresa_user = User.objects.create_user(username='empresaTest1', password='senha@123')
        self.empresa = Empresa.objects.create(
            user=self.empresa_user,
            nome_empresa='Empresa Alpha',
            cnpj='12.345.678/0001-90',
        )

        # Vaga criada pela empresa
        self.vagas = Vagas.objects.create(
            vaga = 'Dev Python',
            descricao = 'Emprego daora, vem.',
            nivel = 'junior',
            localidade = 'Remoto',
            salario = 4000.00,
            empresa = self.empresa
        )

        self.url_candidatura= reverse('candidatar', args=[self.vagas.pk])


    def teste_candidato_acessa_formulario(self):
        self.client.login(username='candidatoTest1', password='senha@123')
        response = self.client.get(self.url_candidatura)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'Candidatura')

    def teste_empresa_acessa_formulario(self):
        self.client.login(username='empresaTest1', password='senha@123')
        response = self.client.get(self.url_candidatura)
        self.assertRedirects(response, reverse('vagas-list'))
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("Empresas não podem se candidatar" in str(m) for m in messages))

    def test_usuario_nao_autenticado(self):
        response = self.client.get(self.url_candidatura)  # Capturar a resposta?
        self.assertRedirects(response, f"/login/?next={self.url_candidatura}")



# Create your tests here.
