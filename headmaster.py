import os

import grades
import messages
import user
from connection import connection


def headmaster_menu(headmaster_id):
    while True:
        os.system('cls')
        user.showUserData(headmaster_id)
        print('1. Uzytkownicy')
        print('2. Klasy i lekcje')
        print('3. Oceny')
        print('4. Wyswietl plan lekcji')
        print('5. Wyswietl logi uzytkownikow')
        print('6. Wyswietl logi ocen')
        print('7. Wyswietl korespondencje')
        print('0. Powrot')
        choice = input('Wybierz : ')
        if choice == '1':
            user.user_action_menu()
            messages.hold()
        if choice == '2':
            class_menu()
            messages.hold()
        if choice == '3':
            grades.grades_menu()
            messages.hold()
        if choice == '4':
            printSchedule()
            messages.hold()
        if choice == '5':
            printUserLogs()
            messages.hold()
        if choice == '6':
            printGradesLogs()
            messages.hold()
        if choice == '7':
            printMessages()
            messages.hold()
        if choice == '0':
            break


def class_menu():
    os.system('cls')
    print('1. Wyswietl plan lekcji')
    print('2. Dodaj nowa klase')
    print('3. Usun klase')
    print('4. Dodaj nowa lekcje')
    print('5. Dodaj lekcje klasie')
    print('6. Usun lekcje')
    print('0. Powrot')
    choice = input('Wybierz : ')
    if choice == '1':
        printSchedule()
        messages.hold()
    if choice == '2':
        addClass()
        messages.hold()
    if choice == '3':
        removeClass()
        messages.hold()
    if choice == '4':
        addNewLesson()
        messages.hold()
    if choice == '5':
        assignLessonToClass()
        messages.hold()
    if choice == '6':
        removeLesson()
        messages.hold()
    if choice == '0':
        pass


def getHeadMasters():
    cursor = connection().cursor()
    condition = 'dyrektor'
    sql = """
            SELECT 
            id_uzytkownika"id",
            imie || ' ' || nazwisko"name"
            FROM uzytkownik
            WHERE typ_uzytkownika = :dyrektor"""
    cursor.execute(sql, {'dyrektor': condition})
    i = 0
    data = []
    for id, name in cursor:
        print(str(i) + '  > ' + str(id) + '  ' + str(name))
        data.append({'id': id, 'name': name})
        i += 1

    headmaster_index = int(input('Wybierz indeks dyrektora : '))
    headmaster = data[headmaster_index]

    print("Wybrany dyrektor : " + headmaster['name'])

    cursor.close()
    connection().close()
    return headmaster['id']


def printUserLogs():
    cursor = connection().cursor()
    sql = """
            SELECT DISTINCT
            id_logu "log_id",
            id_uzytkownika "user_id",
            czas "time",
            komenda "command",
            stare_imie "old_name",
            nowe_imie "new_name",
            stare_nazwisko "old_surname",
            nowe_nazwisko "new_surname",
            stary_wiek "old_age",
            nowy_wiek "new_age",
            stary_numer_telefonu "old_phone_number",
            nowy_numer_telefonu "new_phone_number",
            stary_email "old_email",
            nowy_email "new_email"
            FROM logi_uzytkownikow
            ORDER BY id_logu ASC
            """
    cursor.execute(sql)
    i = 0
    data = []
    for (log_id, user_id, time, command, old_name, new_name, old_surname,
         new_surname, old_age, new_age, old_phone_number, new_phone_number,
         old_email, new_email) in cursor:
        data.append({'log_id': log_id, 'user_id': user_id, 'time': time, 'command': command, 'old_name': old_name,
                     'new_name': new_name, 'old_surname': old_surname, 'new_surname': new_surname, 'old_age': old_age,
                     'new_age': new_age, 'old_phone_number': new_phone_number,
                     'new_phone_number': new_phone_number, 'old_email': old_email, 'new_email': new_email})

    for item in data:
        for key in item:
            if item[key] is None:
                item[key] = 'NULL'

    for item in data:
        print()
        print('NUMER LOGU ' + str(i))
        print('id_logu:\t' + str(item['log_id']))
        print('Czas:\t\t' + str(item['time']))
        print('Komenda:\t' + str(item['command']))
        print('Imie:\t\t', end='')
        print('brak zmian => ' + str(item['old_name']) if str(item['old_name']) == str(item['new_name']) else str(
            item['old_name']) + '->' + str(item['new_name']))
        print('Nazwisko:\t', end='')
        print('brak zmian => ' + str(item['old_surname']) if str(item['old_surname']) == str(
            item['new_surname']) else str(item['old_surname']) + '->' + str(item['new_surname']))
        print('Wiek:\t\t', end='')
        print('brak zmian => ' + str(item['old_age']) if str(item['old_age']) == str(item['new_age']) else str(
            item['old_age']) + '->' + str(item['new_age']))
        print('Nr tel:\t\t', end='')
        print('brak zmian => ' + str(item['old_phone_number']) if str(item['old_phone_number']) == str(
            item['new_phone_number']) else str(item['old_phone_number']) + '->' + str(item['new_phone_number']))
        print('Email:\t\t', end='')
        print('brak zmian => ' + str(item['old_email']) if str(item['old_email']) == str(item['new_email']) else str(
            item['old_email']) + '->' + str(item['new_email']))
        i += 1


def printGradesLogs():
    cursor = connection().cursor()
    sql = """
            SELECT DISTINCT
            id_logu "log_id",
            id_ucznia "user_id",
            id_przedmiotu "subject_id",
            czas "time",
            komenda "command",
            stara_ocena "old_grade",
            nowa_ocena "new_grade",
            stary_opis "old_description",
            nowy_opis "new_description"
            FROM logi_ocen
            ORDER BY id_logu ASC
            """
    cursor.execute(sql)
    i = 0
    data = []
    for (log_id, user_id, subject_id, time, command,
         old_grade, new_grade, old_description, new_description) in cursor:
        data.append({'log_id': log_id, 'user_id': user_id, 'subject_id': subject_id, 'time': time, 'command': command,
                     'old_grade': old_grade, 'new_grade': new_grade, 'old_description': old_description,
                     'new_description': new_description})

    for item in data:
        for key in item:
            if item[key] is None:
                item[key] = 'NULL'

    for item in data:
        print()
        print('NUMER LOGU ' + str(i))
        print('Id logu:\t' + str(item['log_id']))
        print('Przedmiot:\t' + str(item['subject_id']))
        print('Czas:\t\t' + str(item['time']))
        print('Komenda:\t' + str(item['command']))
        print('Ocena:\t\t', end='')
        print('brak zmian => ' + str(item['old_grade']) if str(item['old_grade']) == str(item['new_grade']) else str(
            item['old_grade']) + '->' + str(item['new_grade']))
        print('Opis:\t\t', end='')
        print('brak zmian => ' + str(item['old_description']) if str(item['old_description']) == str(
            item['new_description']) else str(item['old_description']) + '->' + str(item['new_description']))

        i += 1


def printSchedule():
    cursor = connection().cursor()
    sql = """
            SELECT DISTINCT
            k.stopien "classCode",
            bz.id_przedmiotu "subject_id",
            godzina_rozpoczecia"start",
            godzina_zakonczenia"end",
            s.id_sali "roomName"
            FROM klasa k JOIN plan_lekcji pl ON k.id_klasy = pl.id_klasy
            JOIN blok_zajeciowy bz ON pl.id_bloku = bz.id_bloku
            JOIN przedmioty p ON p.id_przedmiotu = bz.id_przedmiotu
            JOIN sala s ON s.id_sali = bz.id_sali
            """
    cursor.execute(sql)
    data = []
    for (classCode, subject_id, start, end, roomName) in cursor:
        data.append({'classCode': classCode, 'subject_id': subject_id, 'start': start.split(':'), 'end': end,
                     'roomName': roomName})
    print('\t Sala\tKod przedmiotu\tRozpoczecie\tZakonczenie')
    for item in sorted(data, key=lambda i: (
            int(i['classCode'][0]), i['classCode'][1], int(i['start'][0]), int(i['start'][1]))):
        print()
        print('Klasa :\t' + str(item['classCode']))
        print('\tSala :\t\t' + str(item['roomName']))
        print('\tId przedmiotu:\t' + str(item['subject_id']))
        print('\tRozpoczecie:\t' + str(item['start'][0]) + ':' + str(item['start'][1]))
        print('\tZakonczenie:\t' + str(item['end']))


def printMessages():
    cursor = connection().cursor()
    sql = """
            SELECT DISTINCT
            u1.imie || ' ' || u1.nazwisko"name1",
            u2.imie || ' ' || u1.nazwisko"name2",
            k.tresc  "message",
            k.czas "time"
            FROM korespondencja k
            JOIN uzytkownik u1 ON u1.id_uzytkownika = k.id_nadawcy
            JOIN uzytkownik u2 ON u2.id_uzytkownika = k.id_odbiorcy
            ORDER BY k.czas DESC
            """
    cursor.execute(sql)
    data = []
    for (name1, name2, message, time) in cursor:
        data.append({'name1': name1, 'name2': name2, 'message': message, 'time': time})

    for item in data:
        print()
        print('Nadawca:\t' + str(item['name1']))
        print('Odbiorca:\t' + str(item['name2']))
        print('Tresc:\t\t' + item['message'])
        print('Data:\t\t' + str(item['time']))


def addClass():
    cursor = connection().cursor()
    print('Istniejace kody klas')
    sql = """
            SELECT DISTINCT
            stopien "classCode"
            FROM klasa
            """
    cursor.execute(sql)
    data = []
    for classCode in cursor:
        data.append({'classCode': classCode[0]})
    for item in sorted(data, key=lambda i: (int(i['classCode'][0]), i['classCode'][1])):
        print('>' + str(item['classCode']))
    classCode = input('Podaj rozniacy sie kod klasy : ')
    if classCode in cursor:
        classCode = input('Podaj rozniacy sie kod klasy : ')
    print('Istniejace profile klas : ')
    sql = """
            SELECT DISTINCT
            profil "spec"
            FROM klasa
            """
    cursor.execute(sql)
    for item in cursor:
        print('>' + str(item[0]))
    spec = input('Podaj profil klasy : ')

    sql = """
            Insert into KLASA(ID_KLASY, STOPIEN, PROFIL)
            values (KLASA_SEQ.NEXTVAL, :classCode, :spec)
            """

    cursor.execute(sql, [classCode, spec])
    connection().commit()
    print('Dodano klase')


def removeClass():
    os.system('cls')
    cursor = connection().cursor()
    sql = """
    SELECT ID_KLASY "id", STOPIEN || ' ' || PROFIL "klasy"
    FROM KLASA
    ORDER BY ID_KLASY
    """
    cursor.execute(sql)

    i = 0
    data = []
    for id, klasy in cursor:
        print(str(i) + ' ' + str(klasy))
        data.append({'id': id})
        i += 1

    try:
        choice = int(input('Wpisz id klasy : '))
    except:
        print('Wpisano bledny nr klasy')

    sql = """
    DELETE FROM PLAN_LEKCJI
    WHERE ID_KLASY = :KLASA
    """
    try:
        cursor.execute(sql, [data[choice]['id']])
    except:
        pass

    sql = """
    UPDATE UZYTKOWNIK
    SET ID_KLASY = NULL
    WHERE ID_KLASY = :klasa
    """
    try:
        cursor.execute(sql, [data[choice]['id']])
    except:
        pass

    sql = """
    DELETE FROM KLASA
    WHERE ID_KLASY = :klasa
    """
    try:
        cursor.execute(sql, [data[choice]['id']])
    except:
        pass

    connection().commit()
    cursor.close()


def removeLesson():
    cursor = connection().cursor()
    print('Klasy :')
    sql = """
            SELECT DISTINCT
            id_klasy "class_id",
            stopien "classCode"
            FROM klasa
            """
    cursor.execute(sql)
    data = []
    for class_id, classCode in cursor:
        data.append({'class_id':class_id, 'classCode':classCode})
    print('ID\tKlasa')
    for item in sorted(data, key=lambda i: (int(i['classCode'][0]), i['classCode'][0])):
        print('>' + str(item['class_id']) + '\t' + item['classCode'])
    class_id = int(input('Podaj id klasy : '))

    

    print('Mozliwe lekcje do usuniecia :')
    sql = """
            SELECT DISTINCT
            pl.id_bloku "lesson_id",
            id_sali "room_id",
            id_przedmiotu "subject_id",
            id_nauczyciela "teacher_id",
            godzina_rozpoczecia "start_hour",
            godzina_zakonczenia "end_hour",
            dzien "day"
            FROM blok_zajeciowy bz
            JOIN plan_lekcji pl ON pl.id_bloku = bz.id_bloku
            WHERE id_klasy = :class_id
            """
    cursor.execute(sql, [class_id])
    data = []
    for lesson_id, room_id, subject_id, teacher_id, start_hour, end_hour, day in cursor:
        data.append({'lesson_id': lesson_id,
                     'room_id': room_id,
                     'subject_id': subject_id,
                     'teacher_id': teacher_id,
                     'start_hour': start_hour.split(':'),
                     'end_hour': end_hour,
                     'day': day})
    print('ID\tSala\tZajecia\tNauczyciel\tGodziny\t\tDzien')
    for item in sorted(data, key=lambda i: (int(i['start_hour'][0]), int(i['start_hour'][1]))):
        item['start_hour'] = item['start_hour'][0]+':'+item['start_hour'][1]
        print('>' + str(item['lesson_id']) + '\t' + str(item['room_id'])
              + '\t' + item['subject_id'] + '\t' + str(item['teacher_id']) + '\t\t' + item['start_hour'] + '-' + item[
                  'end_hour'] + '\t' + str(item['day']))
    lesson_id = int(input('Podaj id lekcji : '))

    sql = """
        DELETE FROM plan_lekcji
        WHERE id_klasy = :class_id
        AND id_bloku = :lesson_id
        """
    try:
        cursor.execute(sql,[class_id,lesson_id])
    except:
        print('Wystapil blad')

    connection().commit()



def addNewLesson():
    cursor = connection().cursor()
    print('Mozliwe sale :')
    sql = """
            SELECT DISTINCT
            id_sali "room_id",
            nazwa "roomName"
            FROM sala
            """
    cursor.execute(sql)
    data = []
    for room_id, roomName in cursor:
        data.append({'room_id': room_id, 'roomName': roomName})
    print('ID\tNazwa')
    for item in sorted(data, key=lambda i: int(i['room_id'])):
        print('>' + str(item['room_id']) + '\t' + item['roomName'])
    room_id = int(input('Podaj id sali : '))

    print('Mozliwe przedmioty :')
    sql = """
            SELECT DISTINCT
            id_przedmiotu "subject_id",
            nazwa "name"
            FROM przedmioty
            """
    cursor.execute(sql)
    data = []
    for subject_id, name in cursor:
        data.append({'subject_id': subject_id, 'name': name})
    print('ID\tNazwa')
    for item in sorted(data, key=lambda i: i['subject_id']):
        print('>' + str(item['subject_id']) + '\t' + item['name'])
    subject_id = input('Podaj id przedmiotu : ')

    print('Mozliwi nauczyciele :')
    sql = """
            SELECT DISTINCT
            id_uzytkownika "user_id",
            imie "name",
            nazwisko "surname"
            FROM uzytkownik
            WHERE uzytkownik.typ_uzytkownika = 'nauczyciel'
            """
    try:
        cursor.execute(sql)
    except:
        print('Wystapil blad')
    
    data = []
    for user_id, name, surname in cursor:
        data.append({'user_id': user_id, 'name': name, 'surname': surname})
    print('ID\tImie i nazwisko')
    for item in sorted(data, key=lambda i: i['surname']):
        print('>' + str(item['user_id']) + '\t' + item['name'] + ' ' + item['surname'])
    teacher_id = int(input('Podaj id nauczyciela : '))

    start_hours = ['8:00', '8:55', '9:45', '10:45', '11:40', '12:35', '13:30']
    end_hours = ['8:45', '9:40', '10:30', '11:30', '12:25', '13:20', '14:15']
    print('godziny rozpoczecia \t', end='')
    print(start_hours)
    print('godziny zakonczenia \t', end='')
    print(end_hours)
    start_hour = input('Wybierz godzine rozpoczecia : ')
    if start_hour not in start_hours:
        start_hour = input('Wybierz poprawna godzine rozpoczecia : ')
    end_hour = input('Wybierz godzine zakonczenia : ')
    if end_hour not in end_hours:
        end_hour = input('Wybierz poprawna godzine zakonczenia : ')

    days = ['poniedzialek', 'wtorek', 'sroda', 'czwartek', 'piatek']
    day = input('Podaj dzien w ktorym odbeda sie zajecia :')
    if day not in days:
        day = input('Podaj poprawny dzien :')
    day = day.upper()
    sql = """
            Insert into BLOK_ZAJECIOWY(ID_BLOKU, ID_SALI, ID_PRZEDMIOTU, ID_NAUCZYCIELA,
            GODZINA_ROZPOCZECIA, GODZINA_ZAKONCZENIA, DZIEN)
            values (BLOK_ZAJECIOWY_SEQ.NEXTVAL, :room_id, :subject_id, :teacher_id, :start_hour, :end_hour, :day)
            """
    try:
        cursor.execute(sql, [room_id, subject_id, teacher_id, start_hour, end_hour, day])
    except:
        print('Wystapil blad')
    
    connection().commit()
    print('Dodano lekcje')


def getClassScheduleForGivenDay(class_id, day):
    cursor = connection().cursor()
    sql = """
            SELECT DISTINCT
            bz.id_bloku "lesson_id",
            id_sali "room_id",
            id_przedmiotu "subject_id",
            id_nauczyciela "teacher_id",
            godzina_rozpoczecia "start_hour",
            godzina_zakonczenia "end_hour",
            dzien "day"
            FROM blok_zajeciowy bz
            JOIN plan_lekcji pl ON pl.id_bloku = bz.id_bloku
            WHERE id_klasy = :class_id
            AND dzien = :day
            """
    cursor.execute(sql, [class_id, day])
    data = []
    for lesson_id, room_id, subject_id, teacher_id, start_hour, end_hour, day in cursor:
        data.append({'lesson_id': lesson_id,
                    'room_id': room_id,
                    'subject_id': subject_id,
                    'teacher_id': teacher_id,
                    'start_hour': start_hour,
                    'end_hour': end_hour,
                    'day': day})
    return data

def assignLessonToClass():
    cursor = connection().cursor()
    print('Mozliwe klasy :')
    sql = """
            SELECT DISTINCT
            id_klasy "class_id",
            stopien "classCode",
            profil "spec"
            FROM klasa
            """
    try:
        cursor.execute(sql)
    except:
        print('Wystapil blad')
    data = []
    for class_id, classCode, spec in cursor:
        data.append({'class_id': class_id, 'classCode': classCode, 'spec': spec})
    print('ID\tKlasa\tProfil')
    for item in sorted(data, key=lambda i: (int(i['classCode'][0]), i['classCode'][1])):
        print('>' + str(item['class_id']) + '\t' + item['classCode'] + '\t' + item['spec'])
    class_id = int(input('Podaj id klasy : '))

    day = input('Podaj dzien : ').upper()

    data = getClassScheduleForGivenDay(class_id, day)

    start_time = []
    if data is not None: 
        for lesson in data:
            start_time.append(lesson['start_hour'])
    all_possible_hours = ['8:00', '8:55', '9:45', '10:45', '11:40', '12:35', '13:30']
    for item in start_time:
        if item in all_possible_hours:
            all_possible_hours.remove(item)
    print('Mozliwe godziny : ',end='')
    print(all_possible_hours)

    data = []
    for beg_hour in all_possible_hours:
        sql = """
                SELECT DISTINCT
                bz.id_bloku "lesson_id",
                id_sali "room_id",
                id_przedmiotu "subject_id",
                id_nauczyciela "teacher_id",
                godzina_rozpoczecia "start_hour",
                godzina_zakonczenia "end_hour",
                dzien "day"
                FROM blok_zajeciowy bz
                WHERE godzina_rozpoczecia = :beg_hour
                AND bz.id_bloku NOT IN (SELECT id_bloku FROM plan_lekcji)
                """
        cursor.execute(sql, [beg_hour])
        for lesson_id, room_id, subject_id, teacher_id, start_hour, end_hour, day in cursor:
            data.append({'lesson_id': lesson_id,
                        'room_id': room_id,
                        'subject_id': subject_id,
                        'teacher_id': teacher_id,
                        'start_hour': start_hour,
                        'end_hour': end_hour,
                        'day': day})
    if len(data) == 0:
        print('Brak zajec do przypisania')
        input('Wcisnij przycisk zeby kontynuowac')
        return
    print('Mozliwe lekcje do przypisania :')
    print('ID\tSala\tZajecia\tNauczyciel\tGodziny\tDzien')
    for item in sorted(data, key=lambda i: i['subject_id']):
        print('>' + str(item['lesson_id']) + '\t' + str(item['room_id'])
              + '\t' + item['subject_id'] + '\t' + str(item['teacher_id']) + '\t' + item['start_hour'] + '-' + item[
                  'end_hour'] + '\t' + str(item['day']))
    lesson_id = input('Podaj id lekcji : ')

    sql = """
            Insert into PLAN_LEKCJI(ID_LEKCJI, ID_KLASY, ID_BLOKU) values (PLAN_LEKCJI_SEQ.NEXTVAL, :class_id, :lesson_id)
            """

    cursor.execute(sql, [class_id, lesson_id])
    connection().commit()
    print('Dodano przypisano zajecia klasie')
