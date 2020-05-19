import os
from connection import connection

currentUser = None


def hold():
    input('Wcisnij przycisk zeby kontunuowac ...')
    os.system('cls')


def edit_grade_menu(data, grade_id):
    while True:
        os.system('cls')
        showGradeData(data)
        print('1. Edytuj opis')
        print('2. Edytuj ocene')
        print('3. Powrot')
        choice = input('Wybierz : ')
        if choice == '1':
            setDescription(grade_id)
            hold()
        if choice == '2':
            setGrade(grade_id)
            hold()
        if choice == '3':
            break


def grades_menu():
    data = getGrades()
    while True:
        for grade in data:
            showGradeData(grade)
        print('1. Edytuj ocene')
        print('2. Usun ocene')
        print('3. Dodaj ocene')
        print('4. Powrot')
        choice = input('Wybierz : ')
        if choice == '4':
            break
        if choice == '1':
            if(len(data)>0):
                index = int(input('Wybierz indeks oceny: '))
                edit_grade_menu(data[index], data[index]['grade_id'])
            else:
                print('Brak ocen do edycji')    
        if choice == '2':
            if(len(data)>0):
                index = int(input('Wybierz indeks oceny: '))
                deleteGrade(data[index]['grade_id'])
            else:
                print('Brak ocen do usunięcia')
            hold()
        if choice == '3':
            addGrade()
            hold()
        else:
            print('Nieporawny wybor')


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


def addGrade():
    os.system('cls')

    cursor = connection().cursor()
    sql = """
            SELECT 
            id_przedmiotu "id",
            nazwa "name",
            stopien "lvl"
            FROM przedmioty
            """
    cursor.execute(sql)
    for id, name, lvl in cursor:
        print(str(id) + '\t' + str(name[:14]) + '.\t' + str(lvl) + '\t')
    
    subjectCode = input('Wprowadz kod przedmiotu (1 kolumna) : ')

    sql = """
            SELECT 
            id_uzytkownika "id",
            imie "firstName",
            nazwisko "lastName",
            stopien "code"
            FROM uzytkownik JOIN klasa ON uzytkownik.id_klasy = klasa.id_klasy
            WHERE typ_uzytkownika='uczen'
            """
    cursor.execute(sql)
    for id, firstName, lastName, code in cursor:
        name = firstName + ' ' + lastName
        if len(name) > 15:
            name = firstName + lastName[3] + '.'
        print(str(id) + '\t' + name + '\t' + str(code) + '\t')
    userId = int(input('Wprowadz id uzytkownika z powyzszych mozliwych : '))

   
    grade = int(input('Podaj ocene: '))
    description = input('Podaj opis: ')

    sql = """
            INSERT INTO OCENY(ID_OCENY, ID_PRZEDMIOTU, ID_UCZNIA, OCENA, OPIS)
            values (OCENY_SEQ.NEXTVAL, :subjectCode , :userId, :grade, :description)
            """
    cursor.execute(sql, [subjectCode, userId, grade, description])
    connection().commit()


def getGrades():
    cursor = connection().cursor()
    sql = """
            SELECT 
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
            """
    cursor.execute(sql)
    data = []
    for grade_id, firstName, lastName, grade, description, subjectName, classCode in cursor:
        data.append({'grade_id': grade_id, 'lastName': lastName, 'firstName': firstName,
                     'grade': grade, 'subjectName': subjectName,
                     'classCode': classCode, 'description': description})

    i = 0
    for item in data:
        print(i)
        print(data[i]['firstName'] + ' ' + data[i]['lastName'])
        print('ID oceny:\t' + str(data[i]['grade_id']))
        print('Ocena:\t\t' + str(data[i]['grade']))
        print('Opis:\t\t' + data[i]['description'])
        print('Nazwa :\t\t' + data[i]['subjectName'])
        print('Klasa :\t\t' + data[i]['classCode'])
        i += 1

    return data


def showGradeData(grade):
    print(grade['firstName'] + ' ' + grade['lastName'])
    print('ID oceny:\t' + str(grade['grade_id']))
    print('Ocena:\t\t' + str(grade['grade']))
    print('Opis:\t\t' + grade['description'])
    print('Nazwa:\t\t' + grade['subjectName'])
    print('Kod klasy:\t' + grade['classCode'])


def setGrade(grade_id):
    newGrade = int(input("Wprowadz nowa ocene : "))
    cursor = connection().cursor()
    sql = """
        UPDATE oceny
        SET ocena = :newGrade
        WHERE id_oceny = :grade_id
    """
    try:
        cursor.execute(sql, [newGrade, grade_id])
        connection().commit()
    except:
        print('Blad zmieniania wartosci')
    finally:
        cursor.close()
        connection().close()


def setDescription(grade_id):
    newDescription = input("Wprowadz nowy opis : ")
    cursor = connection().cursor()
    sql = """
        UPDATE oceny
        SET opis = :newDescription
        WHERE id_oceny = :grade_id
    """
    try:
        cursor.execute(sql, [newDescription, grade_id])
        connection().commit()
    except:
        print('Blad zmieniania opisu')
    finally:
        cursor.close()
        connection().close()
