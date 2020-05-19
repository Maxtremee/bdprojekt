import grades
import messages
import os
import user
from connection import connection


def teacher_menu(teacher_id):
    user.showUserData(teacher_id)
    while True:
        print('1. Wyswietl uczniow')
        print('2. Wyswietl oceny (dodaj, usun)')
        print('3. Wyswietl plan lekcji')
        print('4. Napisz wiadomosc')
        print('5. Napisz wiadomosc do klasy')
        print('6. Skrzynka odbiorcza')
        print('7. Powrot')
        choice = input('Wybierz : ')
        if choice == '1':
            printTeacherStudents(teacher_id)
            messages.hold()
        if choice == '2':
            data = getTeacherMadeGrades(teacher_id)
            teacher_grade_menu(data, teacher_id)
            messages.hold()
        if choice == '3':
            printTeacherSchedule(teacher_id)
            messages.hold()
        if choice == '4':
            messages.sendMessage(teacher_id)
            messages.hold()
        if choice == '5':
            messages.sendMessageToClass(teacher_id)
            messages.hold()
        if choice == '6':
            messages.mailBox(teacher_id)
            messages.hold()
        elif choice == '7':
            break


def teacher_grade_menu(data, teacher_id):
    while True:
        printGrades(data)
        print('1. Edytuj ocene')
        print('2. Dodaj ocene')
        print('3. Usun ocene')
        print('4. Powrot')
        choice = input('Wybor : ')
        if choice == '4':
            break
        if choice == '1':
            if len(data)>0:
                index = int(input('Podaj indeks oceny do edycji: '))
                grades.edit_grade_menu(data[index], data[index]['grade_id'])
            else:
                print('Nie ma ocen do edycji')
            messages.hold()
        if choice == '2':
            addGrade(teacher_id)
            messages.hold()
        if choice == '3':
            if len(data)>0:
                index = int(input('Podaj indeks oceny do usunieca: '))
                deleteGrade(data[index]['grade_id'])
            else:
                print('Nie ma ocen do usunięcia')
            messages.hold()
        else:
            print("Niepoprawny wybor...")


def addGrade(teacher_id):
    os.system('cls')

    cursor = connection().cursor()
    sql = """
            SELECT DISTINCT
            przedmioty.id_przedmiotu "id",
            nazwa "name",
            stopien "lvl"
            FROM przedmioty
            JOIN blok_zajeciowy ON przedmioty.id_przedmiotu = blok_zajeciowy.id_przedmiotu
            WHERE id_nauczyciela = :teacher_id
            """
    cursor.execute(sql, [teacher_id])
    for id, name, lvl in cursor:
        print(str(id) + '\t' + str(name[:14]) + '.\t' + str(lvl) + '\t')
    subjectCode = input('Wprowadz kod przedmiotu (1 kolumna) : ')

    condition = True
    while condition:
        subjectCode = input('Wprowadz kod przedmiotu (1 kolumna) : ')
        try:
            assert subjectCode != id
            condition = False
        except ValueError:
            print('Indeks musi być liczbą')
        except IndexError:
            print('Nie ma takiego indeksu')
        except AssertionError:
            print('Nie ma takiego indeksu')

    students = printTeacherStudents(teacher_id)

    condition = True
    while condition:
        index = input('Wybierz indeks ucznia : ')
        try:
            index = int(index)
            studentId = students[index]['id']
            assert index>=0
            condition = False
        except ValueError:
            print('Indeks musi być liczbą')
        except IndexError:
            print('Nie ma takiego indeksu')
        except AssertionError:
            print('Nie ma takiego indeksu')


    cursor = connection().cursor()
    grade = int(input('Podaj ocene: '))
    description = input('Podaj opis: ')

    sql = """
            INSERT INTO OCENY(ID_OCENY, ID_PRZEDMIOTU, ID_UCZNIA, OCENA, OPIS)
            values (OCENY_SEQ.NEXTVAL, :subjectCode , :studentId, :grade, :description)
            """
    cursor.execute(sql, [subjectCode, studentId, grade, description])
    connection().commit()


def deleteGrade(grade_id):
    cursor = connection().cursor()
    sql = """
        DELETE
        FROM oceny
        WHERE id_oceny = :grade_id
    """
    try:
        cursor.execute(sql, [grade_id])
        connection().commit()
    except:
        print('Blad usuwania')
    finally:
        cursor.close()
        connection().close()


def getTeacherMadeGrades(teacher_id):
    cursor = connection().cursor()
    sql = """
            SELECT DISTINCT
            id_oceny "grade_id",
            imie "firstName",
            nazwisko "lastName",
            ocena "grade",
            opis "description",
            nazwa "subjectName",
            klasa.stopien "classCode"
            FROM uzytkownik 
            JOIN oceny ON oceny.id_ucznia = uzytkownik.id_uzytkownika
            JOIN przedmioty ON przedmioty.id_przedmiotu = oceny.id_przedmiotu
            JOIN klasa ON klasa.id_klasy = uzytkownik.id_klasy
            JOIN blok_zajeciowy ON przedmioty.id_przedmiotu = blok_zajeciowy.id_przedmiotu
            WHERE id_nauczyciela = :teacher_id
            """
    cursor.execute(sql, [teacher_id])
    i = 0
    data = []
    for grade_id, firstName, lastName, grade, description, subjectName, classCode in cursor:
        data.append({'grade_id': grade_id,
                     'lastName': lastName,
                     'firstName': firstName,
                     'grade': grade,
                     'subjectName': subjectName,
                     'classCode': classCode,
                     'description': description})

    return data


def printGrades(data):
    i = 0
    for grade in data:
        print(i)
        print("Uczen :\t\t" + grade['firstName'] + ' ' + grade['lastName'])
        print("Nazwa :\t\t" + grade['subjectName'])
        print("Ocena :\t\t" + str(grade['grade']))
        print("Opis : \t\t" + grade['description'])
        i += 1


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


    condition = True
    while condition:
        teacher_index = input('Wybierz indeks nauczyciela : ')
        try:
            teacher_index = int(teacher_index)
            teacher = data[teacher_index]
            assert teacher_index >=0
            condition = False
        except ValueError:
            print('Indeks musi być liczbą')
        except IndexError:
            print('Nie ma takiego indeksu')
        except AssertionError:
            print('Nie ma takiego indeksu')

    print("wybrany nauczyciel : " + teacher['name'])

    cursor.close()
    connection().close()
    return teacher['id']


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

    cursor.close()
    connection().close()

    return students


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
