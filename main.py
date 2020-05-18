import user, grades, teacher, messages, student, head
import os
from user import *
from connection import connection, check_pwd

def hold():
    input("Wcisnij klawisz zeby kontynuowac...")
    os.system('cls')

def person_menu():
    print('1. Uczen')
    print('2. Nauczyciel')
    print('3. Dyrektor')
    print('4. Zakoncz')
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
    print('2. Dodaj nowego uzytkownika')
    print('3. Wyswietl oceny')
    print('4. Wyswietl plan lekcji')
    print('5. Wyswietl logi uzytkownikow')
    print('6. Wyswietl logi ocen')
    print('7. Wyswietl korespondencje')
    print('8. Powrot')
    choice = input('Wybierz : ')
    return choice


def main_loop():
    check_pwd()
    while True:
        choice = person_menu()
        os.system('cls')
        if choice == '1':
            student_id = student.getStudents()
            while True:
                os.system('cls')
                showUserData(student_id)
                choice = student_menu()
                if choice == '1':
                    student.getStudentGrades(student_id)
                    hold()
                if choice == '2':
                    student.getStudentSchedule(student_id)
                    hold()
                if choice == '3':
                    messages.sendMessage(student_id)
                    hold()
                if choice == '4':
                    messages.mailBox(student_id)
                    hold()
                if choice == '5':
                    break
        elif choice == '2':
            teacher_id = teacher.getTeachers()
            teacher.teacher_menu(teacher_id)
                
        elif choice == '3':
            while True:
                os.system('cls')
                choice = headmaster_menu()
                if choice == '1':
                    user_id = user.getUsers()
                    user.modifyUser(user_id)
                    hold()
                if choice == '2':
                    addNewUser()
                    hold()
                if choice == '3':
                    grades.grades_menu()
                    hold()
                if choice == '4':
                    head.printSchedule()
                    hold()
                if choice == '5':
                    head.printUserLogs()
                    hold()
                if choice == '6':
                    head.printGradesLogs()
                    hold()
                if choice == '7':
                    head.printMessages()
                    hold()
                if choice == '8':
                    break

        elif choice == '4':
            break



main_loop()
