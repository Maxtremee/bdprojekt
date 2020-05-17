import os
from connection import connection
def hold():
    input("Wcisnij przycisk zeby kontynuowac")
    os.system('cls')
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
    sql = """
        SELECT klasa.id_klasy"id", stopien"stopien", profil"profil"
        FROM klasa 
        JOIN plan_lekcji pl ON pl.id_klasy = klasa.id_klasy
        JOIN blok_zajeciowy bz ON bz.id_bloku = pl.id_bloku
        WHERE id_nauczyciela = :id_nauczyciela
        """
    cursor.execute(sql, [id_nauczyciela])
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

