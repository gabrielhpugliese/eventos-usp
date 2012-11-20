import logging

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from google.appengine.api import users
from google.appengine.ext import ndb

import scrape
from models import Evento, Nota


NOTA_ID_FORMAT = '{0}_{1}'


def salvar_eventos(request):
    if not scrape.salvar_eventos():
        return HttpResponse('NOT OK')
    return HttpResponse('OK')


@csrf_exempt
def votar(request, evento):
    nota_valor = request.POST.get('nota')
    user = users.get_current_user()
    if not nota_valor:
        return HttpResponse('NOT OK')

    nota_valor = int(nota_valor) + 1
    nota_id = NOTA_ID_FORMAT.format(evento, user.nickname())
    evento_key = ndb.Key(Evento, evento)
    nota = Nota(id=nota_id, user=user, nota=nota_valor, evento=evento_key)
    nota.put()

    return HttpResponse('OK')


def pegar_nota(request, evento):
    user = users.get_current_user()
    nota_id = NOTA_ID_FORMAT.format(evento, user.nickname())
    nota = ndb.Key(Nota, nota_id).get()

    nota = nota.nota if nota else ''
    return HttpResponse(nota)


def index(request, template='index.html'):
    page = request.GET.get('page')

    eventos = Evento.query().fetch(1000)
    paginator = Paginator(eventos, 10)

    try:
        eventos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        eventos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        eventos = paginator.page(paginator.num_pages)

    template_context = {'eventos': eventos}
    return render_to_response(template, template_context)
