import config
import mysql.connector
import sys
from books import booklist


def InsertBook(bookdata):
    sql = f"insert into {config.mysql['table']} (Booktitle,Author,Price,Genre) values(%s,%s,%s,%s)"
    dataCursor.execute(sql, bookdata)
    con.commit()
 
def PopulateDB():
    for book in booklist:
        bookdata = book[:2] + (int(book[2]),) + book[3:]
        InsertBook(bookdata)

def setupTable(populate = False):
    dataCursor.execute("SHOW TABLES LIKE %s",(config.mysql["table"],))
    result = dataCursor.fetchone()
    if result:
        print(f"Using table {config.mysql['table']}")
        pass
        #TODO: Check Correct Schema
    else:
        print("Table not Found, Setting up a new table")
        dataCursor.execute(f"CREATE TABLE {config.mysql['table']} (Booknumber int UNSIGNED PRIMARY KEY AUTO_INCREMENT,Booktitle varchar(255),Author varchar(255),Price int , Genre varchar(50))")
        if(populate):
            PopulateDB()

try:
    con = mysql.connector.connect(
        host=config.mysql["host"],
        port=3306,
        user=config.mysql["user"],
        password=config.mysql["password"],
        database=config.mysql["database"])
except Exception as e:
    print("There was a error connecting to the servers");
    print(e)
    sys.exit(1)
print("Connection Successful")
dataCursor = con.cursor()

setupTable(dataCursor, populate=True)



