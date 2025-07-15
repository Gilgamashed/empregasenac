from vagas.models import Candidato, Empresa


def is_empresa(user):
    return isinstance(user, Empresa)


def is_candidato(user):
    return isinstance(user, Candidato)