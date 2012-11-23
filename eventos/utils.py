def format_grades(grades):
    grades_dct = {}
    for grade in grades:
        if grade.user not in grades_dct:
            grades_dct[grade.user] = {grade.evento: grade.nota}
        else:
            grades_dct[grade.user][grade.evento] = grade.nota

    return grades_dct
