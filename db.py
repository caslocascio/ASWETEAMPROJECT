import sqlite3
from sqlite3 import Error
import csv

'''
This program db.py organizes the scraped culpa data into a database for
our admin use. It allows us to query upon certain fields, making it
easier to protect our data from API users and create API endpoints for wanted
information. Information includes aspects about courses such as
reviews, workload, etc.
'''

csv_file_name = "culpa.csv"


''' each entry in the CULPADB table includes the professor name, class title,
date, review (inclusive of commentary on both professor and class), workload,
agree (positive feelings toward class and/or professor), disagree (negative
feelings toward class and/or professor), and funny (students tend to be drawn
to classes which include a sense of humor)'''


# creates Table
def init_db():
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


# reads aquired culpa data from csv into database
def create_db():
    f = open(csv_file_name)
    csvreader = csv.reader(f)
    next(csvreader)
    for row in csvreader:
        add_entry(tuple(row))


# add entry into the database where entry is a tuple
def add_entry(entry):
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


'''
entry can assume values like professor name or course title
type can assume values like 'professor' or 'course'
'''


# retrives entry from database based upon desired information
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


# enter professor name
def get_entry_professor(professor):
    return get_entry(professor, "professor")


# enter course title
def get_entry_class(course):
    return get_entry(course, "class")


# enter date of review in form like: 'December 31, 1999'
def get_entry_date(date):
    return get_entry(date, "date")


# enter agreeable rating as a string (typically between 1-5)
def get_entry_agree(agree):
    return get_entry(agree, "agree")


# enter disagreeable rating as a string (typically between 1-5)
def get_entry_disagree(disagree):
    return get_entry(disagree, "disagree")


# enter funny rating as a string (typically between 1-5)
def get_entry_funny(funny):
    return get_entry(funny, "funny")


# clears database
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


if __name__ == '__main__':
    init_db()
