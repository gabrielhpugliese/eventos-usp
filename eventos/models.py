from datetime import datetime

from google.appengine.ext import ndb

GRADE_ID_FORMAT = '{0}_{1}'


class Event(ndb.Model):
    title = ndb.StringProperty()
    link = ndb.StringProperty()
    slug = ndb.StringProperty()
    cost = ndb.StringProperty()
    date_time = ndb.DateTimeProperty()


class Grade(ndb.Model):
    event = ndb.KeyProperty()
    user = ndb.UserProperty()
    value = ndb.IntegerProperty()


class EventFacade(object):
    @staticmethod
    def get_all_events_ordered_since_today():
        return Event.query().filter(Event.date_time >= datetime.now()).order(Event.date_time).fetch(1000)

    @staticmethod
    def save_event(event_id, title, link, slug, cost, date_time):
        event = Event(id=event_id,
                       title=title,
                       link=link,
                       slug=slug,
                       cost=cost,
                       date_time=date_time)
        event.put()


def format_grade_id(event, nickname):
    return GRADE_ID_FORMAT.format(event, nickname)


class GradeFacade(object):
    @staticmethod
    def get_grade_value(event, nickname):
        grade_id = format_grade_id(event, nickname)
        grade = Grade.get_by_id(grade_id, parent=None)

        if grade:
            return grade.value

    @staticmethod
    def get_all_grades():
        return Grade.query().fetch(1000)

    @staticmethod
    def get_grades_from_user(an_user):
        return Grade.query(Grade.user == an_user).fetch(1000)

    @staticmethod
    def save_grade(an_user, grade_value, event):
        grade_id = format_grade_id(event, an_user.nickname())
        event_key = ndb.Key(Event, event)
        grade = Grade(id=grade_id, user=an_user, value=grade_value,
                      event=event_key)
        grade.put()
