import logging
import json

from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from google.appengine.api import users

import scrape
import filtering
import utils
from models import GradeFacade, EventFacade


NOTA_ID_FORMAT = '{0}_{1}'


def recommend(request, template='recommendations.html'):
    ''' Renders a html with all recommendations and grades for the user '''

    my_user = users.get_current_user()
    grades = GradeFacade.get_all_grades()
    grades_dct = utils.format_grades(grades)
    my_voted_events = {grade.evento for grade
                       in GradeFacade.get_grades_from_user(my_user)}
    all_voted_events = {grade.evento for grade in grades}

    filtered_events = filtering.slope_one(my_user, my_voted_events,
                                          all_voted_events, grades_dct)

    recommendations = {}
    for event_key, grade in filtered_events.items():
        event = event_key.get()
        recommendations[event.titulo] = {'info': event, 'grade': grade}

    template_context = {'recommendations': recommendations}
    return render_to_response(template, template_context)


def save_events(request):
    ''' Scrape events from the page and save on db '''

    try:
        events = scrape.save_events_on_db()
    except Exception, e:
        logging.error(str(e))
        return HttpResponseServerError('Error on saving events')
    return HttpResponse('Retrieved {0} events'.format(len(events)))


@csrf_exempt
def vote(request, event):
    ''' Receives a grade as a POST parameter and event as positional in url.
        Saves the grade in db. '''

    grade_value = request.POST.get('grade')
    if not grade_value:
        return HttpResponseServerError('Param grade not found')

    user = users.get_current_user()
    grade_value = int(grade_value) + 1
    GradeFacade.save_grade(user, grade_value, event)

    return HttpResponse('Voted {0} on event {1}'.format(grade_value, event))


def show_grade(request, event):
    ''' Renders the event grade as a json object {'value': int(grade)} '''

    user = users.get_current_user()
    grade_value = GradeFacade.get_grade_value(event, user.nickname())

    response = json.dumps({'value': grade_value})
    return HttpResponse(response, mimetype='application/json')


def index(request, template='index.html'):
    page = request.GET.get('page')

    events = EventFacade.get_all_events()
    paginator = Paginator(events, 10)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = paginator.page(paginator.num_pages)

    template_context = {'events': events}
    return render_to_response(template, template_context)
