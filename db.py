import csv
import bitdotio

'''
This program db.py organizes the scraped culpa data into a database for
our admin use. It allows us to query upon certain fields, making it
easier to protect our data from API users and create API endpoints for wanted
information. Information includes aspects about courses such as
reviews, workload, etc.
'''

csv_file_name = "culpa.csv"
api_key = "UsaA_8UHMCxDTQV483vLM469EpXm"
db_name = "qres_1d5e28b401604bcda36f18114fec4a22_db_writer"


''' each entry in the CULPADB table includes the professor name, class title,
date, review (inclusive of commentary on both professor and class), workload,
agree (positive feelings toward class and/or professor), disagree (negative
feelings toward class and/or professor), and funny (students tend to be drawn
to classes which include a sense of humor)'''


# creates the database
def init_db():
    # if less than 2, the db is empty
    if len(get_all()) < 2:
        return create_db()
    else:
        print("database already exists")
        return True


# reads aquired culpa data from csv into database
# CAUTION: CREATE DB TAKES A VERY LONG TIME, DON'T CALL UNLESS
# DATABASE DOESN'T EXIST
def create_db():
    try:
        conn = bitdotio.bitdotio(api_key).get_connection().cursor()
        f = open(csv_file_name)
        csvreader = csv.reader(f)
        query = "INSERT INTO \"WinstonZhang1999/CULPA\".culpadb VALUES" +\
            " (%s,%s,%s,%s,%s,%s,%s,%s)"
        next(csvreader)
        for row in csvreader:
            print("added: "+str(row))
            conn.execute(query, row)
        conn.close()
        print('Database Online, table populated')
        return True
    except Exception as e:
        print(e)
        return False


# add entry into the database where entry is a tuple
def add_entry(entry):
    try:
        b = bitdotio.bitdotio(api_key)
        conn = b.get_connection().cursor()
        sql_select_query = "INSERT INTO \"WinstonZhang1999/CULPA\".culpadb\
             VALUES" +\
            " (%s,%s,%s,%s,%s,%s,%s,%s)"
        conn.execute(sql_select_query, (entry))
        conn.close()
        print("succesfully added tuple: "+str(clean_tuple(entry)))
        return True
    except Exception as e:
        print(e)
        return False


'''
entry can assume values like professor name or course title
type can assume values like 'professor' or 'course'
'''


# escaping all ' and " for tuple since they break sql
def clean_tuple(entry):
    arr = []
    for index in range(len(entry)):
        str = entry[index]
        arr.append(clean_string(str))
    return tuple(arr)


# escaping all ' and " for a string
def clean_string(entry):
    return (str(entry).replace('\'', '\''+'\'')).replace('\"', '\"'+'\"')


# retrives entry from database based upon desired information
def get_entry(entry, type):
    entry = clean_string(entry)
    try:
        b = bitdotio.bitdotio(api_key)
        conn = b.get_connection()
        c = conn.cursor()
        # print("connected to bitdotio")

        sql_select_query = \
            "SELECT * FROM \"WinstonZhang1999/CULPA\".culpadb" + \
            " WHERE "+type+"=\'"+str(entry)+"\'"
        records = []
        c.execute(sql_select_query, (records))
        records = c.fetchall()

        entries = []
        for e in records:
            entries.append(e)

        c.close()
        conn.close()

        return entries
    except Exception as e:
        print(e)
        return None


# get all entries
def get_all():
    try:
        b = bitdotio.bitdotio(api_key)
        conn = b.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM \"WinstonZhang1999/CULPA\".culpadb")
        records = c.fetchall()

        entries = []
        for entry in records:
            entries.append(entry)

        c.close()
        conn.close()

        return entries
    except Exception as e:
        print(e)
        return None


# clears the database
# CAUTION: DO NOT CLEAR DB UNLESS NECESSARY, RECONSTRUCTION
# TAKES VERY LONG
def clear():
    conn = None
    try:
        conn = bitdotio.bitdotio(api_key).get_connection().cursor()
        conn.execute("DELETE FROM \"WinstonZhang1999/CULPA\".culpadb")
        print('Database Cleared')
    except Exception as e:
        print(e)
        return False

    finally:
        if conn:
            conn.close()
            return True


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


if __name__ == '__main__':
    clear()
    init_db()
