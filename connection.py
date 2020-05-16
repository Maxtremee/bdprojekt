import sys
import cx_Oracle

con = cx_Oracle  # zmienna globalna do przechowywania polaczenia


def check_pwd():
    try:
        sys.argv[1]
    except:
        print('Brak hasła')
        sys.exit()


def est_con():
    pwd = sys.argv[1]
    global con
    con = cx_Oracle.connect("pwr_19_20_L_018248874", pwd, "156.17.43.90", encoding="UTF-8")


def is_connected():
    try:
        con.ping()
        return True
    except:
        return False


def connection():
    if is_connected() is True:
        return con
    else:
        est_con()
        return con
