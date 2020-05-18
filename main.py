import headmaster
import messages
import student
import teacher
from connection import check_pwd
from user import *


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
            headmaster_id = headmaster.getHeadMasters()
            headmaster.headmaster_menu(headmaster_id)

        elif choice == '4':
            break


main_loop()
