import user
from user import *
from connection import connection, check_pwd


def person_menu():
    print('1. Uczen')
    print('2. Nauczyciel')
    print('3. Dyrektor')
    print('4. Zakoncz')
    choice = input('Wybierz : ')
    return choice


def teacher_menu():
    print('1. Wyswietl uczniow')
    print('2. Wyswietl plan lekcji')
    print('3. Napisz wiadomosc')
    print('4. Napisz wiadomosc do klasy')
    print('5. Skrzynka odbiorcza')
    print('6. Powrot')
    choice = input('Wybierz : ')
    return choice


def student_menu():
    print('1. Wyswietl oceny')
    print('2. Wyswietl plan lekcji')
    print('3. Napisz wiadomosc')
    print('4. Skrzynka odbiorcza')
    print('5. Powrot')
    choice = input('Wybierz : ')
    return choice


def headmaster_menu():
    print('1. Wyswietl uzytkownikow')
    print('2. Wyswietl oceny')
    print('3. Wyswietl plan lekcji')
    print('4. Wyswietl logi')
    print('5. Powrot')
    choice = input('Wybierz : ')
    return choice


def main_loop():
    check_pwd()

    while True:
        choice = person_menu()
        os.system('cls')
        if choice == '1':
            student_id = getStudents()
            while True:
                os.system('cls')
                choice = student_menu()
                if choice == '1':
                    getStudentGrades(student_id)
                    hold()
                if choice == '2':
                    getStudentSchedule(student_id)
                    hold()
                if choice == '3':
                    sendMessage(student_id)
                    hold()
                if choice == '4':
                    mailBox(student_id)
                    hold()
                if choice == '5':
                    break
        elif choice == '2':
            teacher_id = getTeachers()
            while True:
                os.system('cls')
                choice = teacher_menu()
                if choice == '1':
                    printTeacherStudents(teacher_id)
                    hold()
                if choice == '2':
                    printTeacherSchedule(teacher_id)
                    hold()
                if choice == '3':
                    sendMessage(teacher_id)
                    hold()
                if choice == '4':
                    sendMessageToClass(teacher_id)
                    hold()
                if choice == '5':
                    mailBox(teacher_id)
                    hold()
                elif choice == '6':
                    break
        elif choice == '3':
            while True:
                os.system('cls')
                choice = headmaster_menu()
                if choice == '1':
                    user_id = user.getUsers()
                    user.modifyUser(user_id)
                    hold()
                if choice == '5':
                    break

        elif choice == '4':
            break


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


def getTeachers():
    cursor = connection().cursor()
    condition = 'nauczyciel'
    sql = """
            SELECT 
            id_uzytkownika"id",
            imie || ' ' || nazwisko"name"
            FROM uzytkownik
            WHERE typ_uzytkownika = :nauczyciel"""
    cursor.execute(sql, {'nauczyciel': condition})
    i = 0
    data = []
    for id, name in cursor:
        print(str(i) + '  > ' + str(id) + '  ' + str(name))
        data.append({'id': id, 'name': name})
        i += 1

    teacher_index = int(input('Wybierz indeks nauczyciela : '))
    teacher = data[teacher_index]

    print("wybrany nauczyciel : " + teacher['name'])

    cursor.close()
    connection().close()
    return teacher['id']


def getStudentGrades(id_ucznia):
    cursor = connection().cursor()
    sql = """
        SELECT nazwa, ocena, opis
        FROM oceny JOIN przedmioty ON
        oceny.id_przedmiotu = przedmioty.id_przedmiotu
        WHERE ID_UCZNIA = :id_ucznia """
    cursor.execute(sql, {'id_ucznia': id_ucznia})
    i = 0
    for subject, grade, opis in cursor:
        print(str(i) + '  > ' + str(subject) + ' > ' + str(grade) + '    ' + opis)
        i += 1
    print('###Koniec listy ocen###')

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

    for item in sorted(data, key=lambda i: (int(i['beg'][0]), int(i['beg'][1]))):
        print(str(i) + '  > ' + str(item['subject']) + ' > ' + str(item['beg'][0] + ':' + item['beg'][1]) + '   ' + str(
            item['end']) + '   ' + str(item['name']))
        i += 1

    cursor.close()
    connection().close()


def sendMessage(id_ucznia):
    cursor = connection().cursor()
    # kwerenda do wyboru wszystkich oprocz siebie
    sql = """
        SELECT id_uzytkownika"id", email, imie || ' ' || nazwisko"name"
        FROM uzytkownik 
        WHERE ID_UZYTKOWNIKA != :id_ucznia """
    cursor.execute(sql, {'id_ucznia': id_ucznia})
    i = 1
    data = []
    for id, email, name in cursor:
        print(str(i) + '  > ' + str(email) + '  ' + str(name))
        data.append({'id': id, 'email': email, 'name': name})
        i += 1

    receiver_id = 0
    receiver_email = input('Wpisz email : ')
    for item in data:
        if item['email'] == receiver_email:
            receiver_id = item['id']

    print('Wysylasz wiadomość do ' + receiver_email)
    message = input('Wprowadz tresc wiadomosci : ')

    sql = """
          INSERT INTO KORESPONDENCJA(ID_KORESPONDENCJI, ID_NADAWCY, ID_ODBIORCY, TRESC)
          values (KORESPONDENCJA_SEQ.NEXTVAL, :sender_id, :receiver_id, :message)"""

    cursor.execute(sql, {'sender_id': id_ucznia, 'receiver_id': receiver_id, 'message': message})
    connection().commit()

    cursor.close()
    connection().close()


def sendMessageToClass(id_nauczyciela):
    cursor = connection().cursor()
    # kwerenda do wyboru wszystkich oprocz siebie
    sql = """
        SELECT id_klasy"id", stopien"stopien", profil"profil"
        FROM klasa 
        """
    cursor.execute(sql)
    i = 1
    data = []
    for id, stopien, profil in cursor:
        print(str(i) + '  > ' + str(stopien) + '  ' + str(profil))
        data.append({'id': id, 'stopien': stopien, 'profil': profil})
        i += 1

    receiver_id = int(input('Wpisz nr klasy : ')) + 99
    receiver_name = ''
    for item in data:
        if item['id'] == receiver_id:
            receiver_name = item['stopien'] + ' ' + item["profil"]
            receiver_id = item['id']

    print('Wysylasz wiadomość do ' + receiver_name)
    sql = """
    SELECT ID_UZYTKOWNIKA"id" FROM UZYTKOWNIK
    WHERE TYP_UZYTKOWNIKA = 'uczen' AND id_klasy = :receiver_id """
    cursor.execute(sql, {'receiver_id': receiver_id})
    message = input('Wprowadz tresc wiadomosci : ')
    data = []
    for id in cursor:
        data.append([id_nauczyciela, id[0], message])
    sql = """
          INSERT INTO KORESPONDENCJA(ID_KORESPONDENCJI, ID_NADAWCY, ID_ODBIORCY, TRESC)
          values (KORESPONDENCJA_SEQ.NEXTVAL, :sender_id, :receiver_id, :message)"""
    cursor.executemany(sql, data)
    connection().commit()

    cursor.close()
    connection().close()


def mailBox(id_receiver):
    cursor = connection().cursor()
    # kwerenda do wyboru wszystkich oprocz siebie
    sql = """
        SELECT id_uzytkownika"id", email, imie || ' ' || nazwisko"name", tresc"message", czas"time"
        FROM korespondencja JOIN uzytkownik ON korespondencja.id_nadawcy = uzytkownik.id_uzytkownika
        WHERE ID_ODBIORCY = :receiver """
    cursor.execute(sql, {'receiver': id_receiver})
    i = 1
    data = []
    for id, email, name, message, time in cursor:
        print(str(i) + '  > ' + str(email) + ' ' + str(time) + '   >->  ' + message[:27] + '...')
        data.append({'id': id, 'email': email, 'name': name, 'time': time, 'message': message})
        i += 1

    print('1. Pokaz wiadomosc ')
    print('2. Powrot')
    choice = input('Wybierz : ')
    if choice == '2':
        return
    elif choice == '1':
        message_index = int(input('Wybierz indeks wiadomosci : ')) - 1
        print('email : ' + data[message_index]['email'] + '\n' + data[message_index]['message'] + '\n')

        print('1. Odpisz na wiadomosc ')
        print('2. Powrot')
        choice = input('Wybierz : ')
        if choice == '2':
            mailBox(id_receiver)
            return
        elif choice == '1':
            message = input('Wprowadz tresc wiadomosci : ')

            sql = """
                INSERT INTO KORESPONDENCJA(ID_KORESPONDENCJI, ID_NADAWCY, ID_ODBIORCY, TRESC)
                values (KORESPONDENCJA_SEQ.NEXTVAL, :sender_id, :receiver_id, :message)"""

            cursor.execute(sql,
                           {'sender_id': id_receiver, 'receiver_id': data[message_index]['id'], 'message': message})
            connection().commit()

    cursor.close()
    connection().close()


def printTeacherStudents(teacher_id):
    cursor = connection().cursor()
    condition = 'uczen'
    sql = """
            SELECT 
            uczen.id_uzytkownika"id",
            uczen.imie || ' ' || uczen.nazwisko"name"
            FROM uzytkownik uczen, uzytkownik nauczyciel
            WHERE uczen.typ_uzytkownika = :student
            AND uczen.id_klasy = nauczyciel.id_klasy
            AND nauczyciel.id_uzytkownika = :teacher_id"""
    cursor.execute(sql, {'student': condition, 'teacher_id': teacher_id})
    i = 0
    students = []
    print('Uczniowie z mojej klasy : ')
    for id, name in cursor:
        print(str(i) + '  > ' + str(id) + '  ' + str(name))
        i += 1
        students.append({'id': id, 'name': name})

    sql = """
            SELECT DISTINCT
            id_uzytkownika"id",
            imie || ' ' || nazwisko"name"
            FROM blok_zajeciowy JOIN plan_lekcji ON blok_zajeciowy.id_bloku = plan_lekcji.id_bloku
            JOIN uzytkownik ON uzytkownik.id_klasy = plan_lekcji.id_klasy
            WHERE id_nauczyciela = :teacher_id
            AND typ_uzytkownika = :uczen"""
    cursor.execute(sql, {'uczen': 'uczen', 'teacher_id': teacher_id})

    print('\n Wszycy uczniowe (takze z poza klasy)')
    for id, name in cursor:
        print(str(i) + '  > ' + str(id) + '  ' + str(name))
        i += 1
        students.append({'id': id, 'name': name})

    print('1. Pokaz oceny')
    print('2. Powrot')
    choice = input('Wybor : ')
    if choice == '1':
        index = int(input('Wybierz indeks studenta : ')) - 1
        student_id = students[index]['id']

        sql = """
            SELECT id_oceny, nazwa, ocena, opis
            FROM oceny JOIN przedmioty ON
            oceny.id_przedmiotu = przedmioty.id_przedmiotu
            WHERE ID_UCZNIA = :student_id """
        cursor.execute(sql, {'student_id': student_id})
        i = 1
        grades = []
        for id_oceny, subject, grade, opis in cursor:
            print(str(i) + '  > ' + str(subject) + ' > ' + str(grade) + '    ' + opis)
            grades.append({'id': id, 'subject': subject, 'grade': grade, 'opis': opis})
            i += 1

        print('1. Modyfikuj ocene')
        print('2. Powrot')
        choice = input('Wybor : ')
        if choice == '2':
            return
        elif choice == '1':
            grade_index = int(input('Wybierz indeks oceny')) - 1
            new_grade = int(input('Nowa ocena : '))
            new_description = input('Opis oceny : ')
            grade_id = grades[grade_index]['id']
            sql = "UPDATE oceny SET ocena = " + str(
                new_grade) + "SET opis = " + new_description + " WHERE id_oceny = " + str(grade_id)
            cursor.execute(sql)
            connection().commit()

    elif choice == '2':
        return

    cursor.close()
    connection().close()


def printTeacherSchedule(teacher_id):
    cursor = connection().cursor()
    sql = """
        SELECT nazwa"subject", godzina_rozpoczecia"beg", godzina_zakonczenia"end", id_klasy
        FROM przedmioty JOIN blok_zajeciowy ON przedmioty.id_przedmiotu = blok_zajeciowy.id_przedmiotu
        JOIN plan_lekcji ON blok_zajeciowy.id_bloku = plan_lekcji.id_bloku
        WHERE id_nauczyciela = :teacher """

    cursor.execute(sql, {'teacher': teacher_id})
    i = 1
    data = []
    for subject, beg, end, name in cursor:
        data.append({'subject': subject, 'beg': beg.split(':'), 'end': end, 'name': name})

    for item in sorted(data, key=lambda i: (int(i['beg'][0]), int(i['beg'][1]))):
        print(str(i) + '  > ' + str(item['subject']) + ' > ' + str(item['beg'][0] + ':' + item['beg'][1]) + '   ' + str(
            item['end']) + '   ' + str(item['name']))
        i += 1

    cursor.close()
    connection().close()


main_loop()
