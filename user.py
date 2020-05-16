import os
from connection import connection


def change_userdata_menu():
    print('1. Zmien imie')
    print('2. Zmien nazwisko')
    print('3. Zmien wiek')
    print('4. Zmien ID klasy')
    print('5. Zmien numer telefonu')
    print('6. Zmien adres email')
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
    return user['id'][0]


def showUserData(user_id):
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
    for id, firstName, lastName, age, user_type, id_class, number, email in cursor:
        print(str(firstName) + ' ' + str(lastName))
        print('ID uzytkownika:\t' + str(id))
        print('Wiek:\t\t' + str(age))
        print('Typ:\t\t' + str(user_type))
        print('ID klasy:\t' + str(id_class))
        print('Numer telefonu:\t' + str(number))
        print('Email:\t\t' + str(email))


def modifyUser(user_id):
    while True:
        os.system('cls')
        showUserData(user_id)
        choice = change_userdata_menu()
        if choice == '1':
            pass
