import os
from connection import connection

currentUser = None


def hold():
    input('Wcisnij przycisk zeby kontunuowac ...')
    os.system('cls')


def change_userdata_menu():
    print('1. Zmien imie')
    print('2. Zmien nazwisko')
    print('3. Zmien wiek')
    print('4. Zmien ID klasy')
    print('5. Zmien numer telefonu')
    print('6. Zmien adres email')
    print('7. Wyjdz')
    choice = input('Wybierz : ')
    return choice


def getUsers():
    cursor = connection().cursor()
    sql = """
            SELECT 
            id_uzytkownika"id"
            FROM uzytkownik
            ORDER BY id_uzytkownika ASC"""
    cursor.execute(sql)
    i = 0
    data = []
    for id in cursor:
        print(str(i))
        showUserData(id[0])
        data.append({'id': id})
        i += 1

    user_index = int(input('Wybierz indeks uzytkownika : '))
    user = data[user_index]

    cursor.close()
    connection().close()
    global currentUser
    currentUser = getUser(user['id'][0])
    return user['id'][0]


def getUser(user_id):
    cursor = connection().cursor()
    sql = """
            SELECT 
            id_uzytkownika "id",
            imie "firstName",
            nazwisko "lastName",
            wiek "age",
            typ_uzytkownika "user_type",
            id_klasy "id_class",
            numer_telefonu "number",
            email "email"
            FROM uzytkownik WHERE id_uzytkownika = :user_id """
    cursor.execute(sql, {'user_id': user_id})
    data = []
    for id, firstName, lastName, age, user_type, id_class, number, email in cursor:
        data.append({'id': id, 'lastName': lastName, 'firstName': firstName,
                     'user_type': user_type, 'id_class': id_class, 'number': number,
                     'email': email, 'age': age})
    return data


def showUserData(user_id):
    userData = getUser(user_id)
    user = userData[0]
    print(user['firstName'] + ' ' + user['lastName'])
    print('ID uzytkownika:\t' + str(user['id']))
    print('Wiek:\t\t' + str(user['age']))
    print('Typ:\t\t' + user['user_type'])
    print('ID klasy:\t' + str(user['id_class']))
    print('Numer telefonu:\t' + user['number'])
    print('Email:\t\t' + user['email'])


def setFirstName(user_id):
    print('Aktualna wartosc : ' + currentUser[0]['firstName'])
    newFirstName = input("Wprowadz nowe imie : ")
    cursor = connection().cursor()
    sql = """
        UPDATE uzytkownik
        SET imie = :newFirstName
        WHERE id_uzytkownika = :user_id
    """
    try:
        cursor.execute(sql, [newFirstName, user_id])
        connection().commit()
    except:
        print('Blad zmieniania wartosci')
    finally:
        cursor.close()
        connection().close()


def setLastName(user_id):
    print('Aktualna wartosc : ' + currentUser[0]['lastName'])
    newLastName = input("Wprowadz nowe nazwisko : ")
    cursor = connection().cursor()
    sql = """
        UPDATE uzytkownik
        SET nazwisko = :newLastName
        WHERE id_uzytkownika = :user_id
    """
    try:
        cursor.execute(sql, [newLastName, user_id])
        connection().commit()
    except:
        print('Blad zmieniania wartosci')
    finally:
        cursor.close()
        connection().close()


def setAge(user_id):
    print('Aktualna wartosc : ' + currentUser[0]['age'])
    newAge = int(input("Wprowadz nowy wiek : "))
    cursor = connection().cursor()
    sql = """
        UPDATE uzytkownik
        SET wiek = :newAge
        WHERE id_uzytkownika = :user_id
    """
    try:
        cursor.execute(sql, [newAge, user_id])
        connection().commit()
    except:
        print('Blad zmieniania wartosci')
    finally:
        cursor.close()
        connection().close()


def setClassID(user_id):
    print('Aktualna wartosc : ' + currentUser[0]['id_class'])
    newIDclass = input("Wprowadz nowe ID klasy : ")
    cursor = connection().cursor()
    sql = """
        UPDATE uzytkownik
        SET id_klasy = :newIDclass
        WHERE id_uzytkownika = :user_id
    """
    try:
        cursor.execute(sql, [newIDclass, user_id])
        connection().commit()
    except:
        print('Blad zmieniania wartosci')
    finally:
        cursor.close()
        connection().close()


def setPhoneNumber(user_id):
    print('Aktualna wartosc : ' + currentUser[0]['number'])
    newNumber = input("Wprowadz nowy numer telefonu : ")
    cursor = connection().cursor()
    sql = """
        UPDATE uzytkownik
        SET numer_telefonu = :newNumber
        WHERE id_uzytkownika = :user_id
    """
    try:
        cursor.execute(sql, [newNumber, user_id])
        connection().commit()
    except:
        print('Blad zmieniania wartosci')
    finally:
        cursor.close()
        connection().close()


def setEmail(user_id):
    print('Aktualna wartosc : ' + currentUser[0]['email'])
    newEmail = input("Wprowadz nowy adres email : ")
    cursor = connection().cursor()
    sql = """
        UPDATE uzytkownik
        SET email = :newEmail
        WHERE id_uzytkownika = :user_id
    """
    try:
        cursor.execute(sql, [newEmail, user_id])
        connection().commit()
    except:
        print('Blad zmieniania wartosci')
    finally:
        cursor.close()
        connection().close()


def modifyUser(user_id):
    while True:
        os.system('cls')
        showUserData(user_id)
        choice = change_userdata_menu()
        if choice == '1':
            setFirstName(user_id)
            hold()
        if choice == '2':
            setLastName(user_id)
            hold()
        if choice == '3':
            setAge(user_id)
            hold()
        if choice == '4':
            setClassID(user_id)
            hold()
        if choice == '5':
            setPhoneNumber(user_id)
            hold()
        if choice == '6':
            setEmail(user_id)
            hold()
        if choice == '7':
            break
