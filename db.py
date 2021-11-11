import sqlite3
from sqlite3 import Error
import csv

'''
Initializes the Table GAME
Do not modify
'''

csv_file_name = "culpa.csv"


#USAGE:
#   db.py uses sqlite3, the database is named CULPADB
#   inside the table contains entries of tuples.
#   Namely, in this format:
#   (professor, class, date, review, workload, agree, disagree, funny)
#
#   TO USE DB: call init_tb()
#
#   TO USE GET ENTRY: call get_entry_'type'('parameter') 
#       with type being a the category (prof, class, etc) and parameter being a string
#       ---> returns a list of tuples
def init_db():
    # creates Table
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute('CREATE TABLE CULPADB(professor TEXT, class TEXT,' +
                     'date TEXT, review TEXT, workload TEXT' +
                     ', agree TEXT, disagree TEXT, funny TEXT)')
        create_db()
        print('Database Online, table created')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


def create_db():
    f = open(csv_file_name)
    csvreader = csv.reader(f)
    next(csvreader)
    for row in csvreader:
            add_entry(tuple(row))


def add_entry(entry):  # will take in a tuple
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute("INSERT INTO CULPADB VALUES "+str(entry))
        conn.commit()
        conn.close()
        print('database online, adding tuple: '+str(entry))
        return True
    except Error as e:
        print(e)
        return False


def get_entry(entry, type):
    try:
        conn = sqlite3.connect('sqlite_db')
        c = conn.cursor()
        print("connected to SQLite")

        sql_select_query = "SELECT * FROM CULPADB WHERE " + type + " = ?"
        c.execute(sql_select_query, (entry,))
        records = c.fetchall()

        entries = []
        for entry in records:
            entries.append(entry)

        c.close()
        conn.close()
        
        return entries
    except Error as e:
        print(e)
        return None


def get_entry_professor(professor):
    return get_entry(professor, "professor")
    

def get_entry_class(course):
    return get_entry(course, "class")

def get_entry_date(date):
    return get_entry(date, "date")

def get_entry_agree(agree):
    return get_entry(agree, "agree")

def get_entry_disagree(disagree):
    return get_entry(disagree, "disagree")

def get_entry_funny(funny):
    return get_entry(funny, "funny")


def clear():
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute("DROP TABLE CULPADB")
        print('Database Cleared')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()

'''
if __name__ == '__main__':
    init_db()
    print('=======================test=====================================')
    print('----------------------------------------------------------------')
    print('get all Aaron Fox entries: ')
    lista = get_entry_professor('Aaron Fox')
    for dup in lista:
        print(dup)
        print()
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    print('get all Introduction to Urban Studies')
    listb = get_entry_class('Introduction to Urban Studies')
    for dup in listb:
        print(dup)
        print()
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    print('get all December 31, 1999')
    listc = get_entry_date('December 31, 1999')
    for dup in listc:
        print(dup)
        print()
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    print('get all funny = 5')
    liste = get_entry_funny('5')
    for dup in liste:
        print(dup)
        print()
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    print('get all agree = 1')
    listf = get_entry_agree('1')
    for dup in listf:
        print(dup)
        print()
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    print('get all disagree = 2')
    listg = get_entry_disagree('2')
    for dup in listg:
        print(dup)
        print()
    print('----------------------------------------------------------------')
    clear()
'''
