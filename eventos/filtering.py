def slope_one(my_user, my_voted_events, all_voted_events, grades_dct):
    """ Returns recommendations through slope one method

    Keyword arguments:
    my_user -- user to recommend
    my_voted_events (set) -- events user already voted
    all_voted_events (set) -- events voted by everyone
    grades_dct (dict) -- dict which key is user and value is a dict containing
                         the event as key and grade as value

    """

    recommendations = {}
    my_non_voted_events = all_voted_events - my_voted_events
    for non_voted_event_key in my_non_voted_events:
        total_count = 0
        total_summ = 0
        for event_key in all_voted_events:
            count = 0
            summ = 0
            for user in grades_dct.keys():
                if user == my_user:
                    continue
                summ += (grades_dct[user][non_voted_event_key] -
                         grades_dct[user][event_key])
                count += 1

            if count > 0:
                try:
                    summ = (summ + grades_dct[my_user][event_key]) * count
                    total_summ += float(summ) / float(count)
                    total_count += count
                except KeyError:
                    continue

        if total_count > 0:
            recommendations[non_voted_event_key] = int(float(total_summ) /
                                                       float(total_count))

    return recommendations

