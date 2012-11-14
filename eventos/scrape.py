from datetime import datetime

import requests
from django.conf import settings

from eventos.models import Evento


def salvar_eventos():
    data = {'action': 'aeh_show_ajax',
            'aeh_search_custo': 'todos',
            'aeh_search_campi': 'todos',
            'aeh_search_page': 1,
            'aeh_search_per_page': 100}
    r = requests.post(settings.SCRAPE_URL, data=data)
    if r.status_code != 200:
        return

    posts = r.json['posts']
    for post in posts:
        evento = Evento(id=post['link'].split('/?events=')[1],
                        titulo=post['titulo'],
                        link=post['link'],
                        tipo_slug=post['tipo_slug'],
                        custo=post['custo'],
                        data_hora=datetime.strptime(post['data_hora'],
                                                    '%d-%m-%Y %H:%M'))
        evento.put()
        break

    return posts
