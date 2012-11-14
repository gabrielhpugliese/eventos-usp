from google.appengine.ext import ndb


class Evento(ndb.Model):
    titulo = ndb.StringProperty()
    link = ndb.StringProperty()
    tipo_slug = ndb.StringProperty()
    custo = ndb.StringProperty()
    data_hora = ndb.DateTimeProperty()


class Nota(ndb.Model):
    evento = ndb.KeyProperty()
    user = ndb.UserProperty()
    nota = ndb.IntegerProperty()
