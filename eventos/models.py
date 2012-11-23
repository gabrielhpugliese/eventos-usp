from google.appengine.ext import ndb

GRADE_ID_FORMAT = '{0}_{1}'


class Event(ndb.Model):
    titulo = ndb.StringProperty()
    link = ndb.StringProperty()
    tipo_slug = ndb.StringProperty()
    custo = ndb.StringProperty()
    data_hora = ndb.DateTimeProperty()


class Grade(ndb.Model):
    evento = ndb.KeyProperty()
    user = ndb.UserProperty()
    nota = ndb.IntegerProperty()


class EventFacade(object):
    @staticmethod
    def get_all_events():
        return Event.query().fetch(1000)

    @staticmethod
    def save_event(event_id, title, link, slug, cost, date_time):
        event = Event(id=event_id,
                       titulo=title,
                       link=link,
                       tipo_slug=slug,
                       custo=cost,
                       data_hora=date_time)
        event.put()


def format_grade_id(event, nickname):
    return GRADE_ID_FORMAT.format(event, nickname)


class GradeFacade(object):
    @staticmethod
    def get_grade_value(event, nickname):
        grade_id = format_grade_id(event, nickname)
        grade = Grade.get_by_id(grade_id, parent=None)

        if grade:
            return grade.nota

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
        grade = Grade(id=grade_id, user=an_user, nota=grade_value,
                     evento=event_key)
        grade.put()
