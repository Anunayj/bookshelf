import config
import mysql.connector
import sys
from books import booklist
from time import sleep

def InsertBook(bookdata):
    sql = f"insert into {config.mysql['table']} (Booktitle,Author,Price,Genre) values(%s,%s,%s,%s)"
    dataCursor.execute(sql, bookdata)
    con.commit()
 
def PopulateDB():
    for book in booklist:
        bookdata = book[:2] + (int(book[2]),) + book[3:]
        InsertBook(bookdata)

def setupTable():
    dataCursor.execute("SHOW TABLES LIKE %s",(config.mysql["table"],))
    result = dataCursor.fetchone()
    if result:
        print(f"Using table {config.mysql['table']}")
        pass
        #TODO: Check Correct Schema
    else:
        print("Table not Found, Setting up a new table")
        dataCursor.execute(f"CREATE TABLE {config.mysql['table']} (Booknumber int UNSIGNED PRIMARY KEY AUTO_INCREMENT,Booktitle varchar(255),Author varchar(255),Price int , Genre varchar(50))")
        while True:
            answer = input("Do you want to populate the Database with Demo Data? (y/n): ")
            if(answer == "y" or answer == "Y"):
                PopulateDB()
                break
            elif(answer == "n" or answer == "N"):
                break
            else:
                print("Invalid Response")
        print("Table Successfully Setup")

def handleInsert():
    print()
    print("Insert a Book")
    Booktitle = input("Enter the title of the book: ")
    Author = input("Enter the name of the Author: ")
    Price = int(input("Enter the price for the book: "))
    Genre = input("Enter the genre of the book: ")
    answer = input("Are you sure you want to insert This book? (y/n): ")
    if(answer=="y" or answer =="Y"):
        InsertBook((Booktitle,Author,Price,Genre))
        print("Book successfully inserted")
    else:
        print("Cancelling transaction")

def handleUpdate():
    pass
def handleDelete():
    pass
def handleSearch():
    pass
def printRecords():
    pass

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

setupTable()


while True:
    sleep(1) #Computers are crazy fast
    # TODO: Make this more better
    print("\nWelcome to Bookshelf, What would you like to do?")
    print("0. Show records")
    print("1. Insert Records")
    print("2. Update Records")
    print("3. Delete Records")
    print("4. Search")
    print("q. Quit")
    
    choice = input("What would you like to do? (1/2/3/4/5/q): ")
    if choice == "0":
        printRecords()
    if choice == "1":
        handleInsert()
    elif choice == "2":
        handleUpdate()
    elif choice == "3":
        handleDelete()
    elif choice == "4":
        handleSearch()
    elif choice == "q":
        break
    else:
        print("Invalid Input!!")
con.commit()
con.close()

