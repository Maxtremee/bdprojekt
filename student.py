from connection import connection
from messages import hold


def getStudentGrades(id_ucznia):
    cursor = connection().cursor()
    sql = """
        SELECT nazwa, ocena, opis
        FROM oceny JOIN przedmioty ON
        oceny.id_przedmiotu = przedmioty.id_przedmiotu
        WHERE ID_UCZNIA = :id_ucznia """
    cursor.execute(sql, {'id_ucznia': id_ucznia})
    i = 0
    print('L.p\tPrzedmiot\tOcena\tOpis')
    for subject, grade, opis in cursor:
        print(str(i) + '\t' + str(subject) + '\t' + str(grade) + '\t' + opis)
        i += 1

    cursor.close()
    connection().close()


def getStudentSchedule(id_ucznia):
    cursor = connection().cursor()
    sql = """
        SELECT nazwa"subject", godzina_rozpoczecia"beg", godzina_zakonczenia"end", u2.imie || ' ' || u2.nazwisko"name"
        FROM przedmioty JOIN blok_zajeciowy ON przedmioty.id_przedmiotu = blok_zajeciowy.id_przedmiotu
        JOIN plan_lekcji ON plan_lekcji.id_bloku = blok_zajeciowy.id_bloku
        JOIN uzytkownik u1 ON u1.id_klasy = plan_lekcji.id_klasy
        JOIN uzytkownik u2 ON u2.id_uzytkownika = blok_zajeciowy.id_nauczyciela
        WHERE u1.ID_UZYTKOWNIKA = :id_ucznia """
    cursor.execute(sql, {'id_ucznia': id_ucznia})
    i = 1
    data = []
    for subject, beg, end, name in cursor:
        data.append({'subject': subject, 'beg': beg.split(':'), 'end': end, 'name': name})

    print('Przedmiot\tRozp.\tZak.\tNauczyciel')
    for item in sorted(data, key=lambda i: (int(i['beg'][0]), int(i['beg'][1]))):
        print('>' + str(item['subject'])[0:14] + '\t' +
              str(item['beg'][0] + ':' + str(item['beg'][1])) + '\t' +
              str(item['end']) + '\t' + str(item['name']))
        i += 1

    cursor.close()
    connection().close()


def getStudents():
    cursor = connection().cursor()
    condition = 'uczen'
    sql = """
            SELECT 
            id_uzytkownika"id",
            imie || ' ' || nazwisko"name"
            FROM uzytkownik
            WHERE typ_uzytkownika = :uczen"""
    cursor.execute(sql, {'uczen': condition})
    i = 0
    data = []
    for id, name in cursor:
        print(str(i) + '  > ' + str(id) + '  ' + str(name))
        i += 1
        data.append({'id': id, 'name': name})
    student_index = int(input('Wybierz indeks ucznia : '))
    student = data[student_index]
    print("wybrany student : " + student['name'])
    hold()
    cursor.close()
    connection().close()
    return student['id']
