from models import Nota


def get_notas():
    notas = Nota.query().filter().fetch(1000)
    notas_dct = {}
    for nota in notas:
        if nota.user not in notas_dct:
            notas_dct[nota.user] = {nota.evento: nota.nota}
        else:
            notas_dct[nota.user][nota.evento] = nota.nota

    return notas_dct


my_user = users.get_current_user()
dct = get_notas()
want = ndb.Key(Evento, 'abertas-as-inscricoes-para-o-primeiro-congresso-de-oncologia-clinica-da-fmrp')
all_eventos = [evento.key for evento in Evento.query().fetch(1000)
               if evento.key != want]

total_count = 0
total_summ = 0
for evento_key in all_eventos:
    count = 0
    summ = 0
    for user in dct.keys():
        try:
            summ += dct[user][want] - dct[user][evento_key]
            count += 1
        except KeyError:
            continue

    if count > 0:
        try:
            total_summ += float(summ) / float(count) + dct[my_user][evento_key] + count
            total_count += count
        except KeyError:
            continue

print total_summ, total_count, float(total_summ) / float(total_count)
