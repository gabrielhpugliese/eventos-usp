from datetime import datetime

import requests
from django.conf import settings

from eventos.models import EventFacade


def save_events_on_db():
    ''' Scrapes the events from json and save them on db. '''

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
        post_id = post['link'].split('/?events=')[1]
        date_time = datetime.strptime(post['data_hora'], '%d-%m-%Y %H:%M')

        EventFacade.save_event(post_id,
                               post['titulo_title'],
                               post['link'],
                               post['tipo_slug'],
                               post['custo'],
                               date_time)

    return posts
