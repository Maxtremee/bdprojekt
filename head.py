from connection import connection
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
            """
    cursor.execute(sql)
    i = 0
    data = []
    for (log_id, user_id, time, command, old_name, new_name, old_surname,
        new_surname, old_age, new_age, old_phone_number, new_phone_number,
        old_email, new_email) in cursor:
        data.append({'log_id':log_id, 'user_id':user_id, 'time':time, 'command':command, 'old_name':old_name,
        'new_name':new_name, 'old_surname':old_surname, 'new_surname':new_surname, 'old_age':old_age, 'new_age':new_age, 'old_phone_number':new_phone_number,
        'new_phone_number':new_phone_number, 'old_email':old_email, 'new_email':new_email})

    for item in data:
        for key in item:
            if item[key] is None:
                item[key] = 'NULL'

    for item in data:
        print()
        print('NUMER LOGU ' + str(i))
        print('id_logu:\t' + str(item['log_id']))
        print('Czas:\t\t'+ str(item['time']))
        print('Komenda:\t' + str(item['command']))
        print('Imie:\t\t',end='')
        print('brak zmian => ' + str(item['old_name']) if str(item['old_name']) == str(item['new_name']) else str(item['old_name']) +'->'+ str(item['new_name']))
        print('Nazwisko:\t',end='')
        print('brak zmian => ' + str(item['old_surname']) if str(item['old_surname']) == str(item['new_surname']) else str(item['old_surname']) +'->'+ str(item['new_surname']))
        print('Wiek:\t\t',end='')
        print('brak zmian => ' + str(item['old_age']) if str(item['old_age']) == str(item['new_age']) else str(item['old_age']) +'->'+ str(item['new_age']))
        print('Nr tel:\t\t',end='')
        print('brak zmian => ' + str(item['old_phone_number']) if str(item['old_phone_number']) == str(item['new_phone_number']) else str(item['old_phone_number']) +'->'+ str(item['new_phone_number']))
        print('Email:\t\t',end='')
        print('brak zmian => ' + str(item['old_email']) if str(item['old_email']) == str(item['new_email']) else str(item['old_email']) +'->'+ str(item['new_email']))
        i+=1


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
            """
    cursor.execute(sql)
    i = 0
    data = []
    for (log_id, user_id, subject_id, time, command, 
        old_grade, new_grade, old_description, new_description) in cursor:
        data.append({'log_id':log_id, 'user_id':user_id,'subject_id':subject_id, 'time':time, 'command':command, 
        'old_grade':old_grade, 'new_grade':new_grade, 'old_description':old_description, 'new_description':new_description})

    for item in data:
        for key in item:
            if item[key] is None:
                item[key] = 'NULL'

    for item in data:
        print()
        print('NUMER LOGU ' + str(i))
        print('Id logu:\t' + str(item['log_id']))
        print('Przedmiot:\t' + str(item['subject_id']))
        print('Czas:\t\t'+ str(item['time']))
        print('Komenda:\t' + str(item['command']))
        print('Ocena:\t\t', end='')
        print('brak zmian => ' + str(item['old_grade']) if str(item['old_grade']) == str(item['new_grade']) else str(item['old_grade']) +'->'+ str(item['new_grade']))
        print('Opis:\t\t', end='')
        print('brak zmian => ' + str(item['old_description']) if str(item['old_description']) == str(item['new_description']) else str(item['old_description']) +'->'+ str(item['new_description']))

        i+=1

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
        data.append({'classCode':classCode, 'subject_id':subject_id, 'start':start.split(':'), 'end':end, 'roomName':roomName})

    for item in sorted(data, key=lambda i: (int(i['classCode'][0]), i['classCode'][1], int(i['start'][0]), int(i['start'][1]))):
        print()
        print('Klasa :\t' + str(item['classCode']))
        print('\tSala :\t\t' + str(item['roomName']))
        print('\tId przedmiotu:\t' + str(item['subject_id']))
        print('\tRozpoczecie:\t'+ str(item['start'][0])+':'+str(item['start'][1]))
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
            """
    cursor.execute(sql)
    data = []
    for (name1, name2, message, time) in cursor:
        data.append({'name1':name1, 'name2':name2, 'message':message, 'time':time})

    for item in data:
        print()
        print('Nadawca:\t' + str(item['name1']))
        print('Odbiorca:\t' + str(item['name2']))
        print('Tresc:\t\t'+ item['message'])
        print('Data:\t\t' + str(item['time']))