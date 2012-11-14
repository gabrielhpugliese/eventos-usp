from django.http import HttpResponse

from google.appengine.api import users
from google.appengine.ext import ndb

import scrape
from models import Evento, Nota


NOTA_ID_FORMAT = '{0}_{1}'


def salvar_eventos(request):
    if not scrape.salvar_eventos():
        return HttpResponse('NOT OK')
    return HttpResponse('OK')


def votar(request, evento):
    print evento
    nota_valor = request.GET.get('nota')
    user = users.get_current_user()
    if not nota_valor:
        return HttpResponse('NOT OK')

    nota_valor = int(nota_valor)
    nota_id = NOTA_ID_FORMAT.format(evento, user.nickname())
    evento_key = ndb.Key(Evento, evento)
    nota = Nota(id=nota_id, user=user, nota=nota_valor, evento=evento_key)
    nota.put()

    return HttpResponse('OK')


def pegar_nota(request, evento):
    user = users.get_current_user()
    nota_id = NOTA_ID_FORMAT.format(evento, user.nickname())
    nota = ndb.Key(Nota, nota_id).get()

    return HttpResponse(nota.nota)
