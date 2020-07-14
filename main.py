import config
import mysql.connector
import sys
from books import booklist
from time import sleep
from tabulate import tabulate

def ask(question):
    while True:
        answer = input(question + " (y/n): ")
        if(answer == "y" or answer == "Y"):
            return True
        elif(answer == "n" or answer == "N"):
            return False
        else:
            print("Invalid Response!")

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
        if(ask("Do you want to populate the Database with Demo Data?")):
            PopulateDB()
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
    print()
    print("Update Book Database:")
    if(not ask("Do you know the Book Id of the entry you want to update?")):
        print("Launching search....")
        while handleSearch():
            pass
    BookNum = input("Enter Book's id you want to update, q to quit: ") 
    if BookNum == "q" or BookNum == "Q":
        return()
    else:
        dataCursor.execute(f"select * from {config.mysql['table']} where Booknumber = %s",(BookNum,)) 
        data = [("Book ID","Name","Author","Price","Genre"),dataCursor.fetchone()]
    if(len(data)==1):
        print("No book With that Bookid")
        return()
    print()
    print("Selected Entry:")
    print(tabulate(data,headers="firstrow",tablefmt="github"))
    dict = {
        "1":"Booktitle",
        "2":"Author",
        "3":"Price",
        "4":"Genre"
    }
    while True:
        print()
        print("Which Field would you like to change")
        print("1. Name")
        print("2. Author")
        print("3. Price")
        print("4. Genre")
        print("b. Update Another book")
        print("m. Return to main Menu")
        ans = input("(1,2,3,4,b,m): ")
        if(ans == "b"):
            return(True)
        elif(ans == "m"):
            return(False)
        elif(ans in dict.keys()):
            pass
            value = input("Enter The new value for the field: ")
            if(ask("Are you sure you want to change that?")):
                dataCursor.execute(f"UPDATE {config.mysql['table']} SET {dict[ans]} = %s WHERE Booknumber = %s",(value if ans not in [3] else int(value),int(BookNum))) 
                con.commit()
                print("Field Successfuly changed to:")
                dataCursor.execute(f"select * from {config.mysql['table']} where Booknumber = %s",(BookNum,)) 
                data = [dataCursor.fetchone()]
                print(tabulate(data,headers=("Book ID","Name","Author","Price","Genre"),tablefmt="github"))
            else:
                print("Cancelling Update")
        else:
            print("Invalid Input!")

         
def handleDelete():
    if(not ask("Do you know the Book Id of the entry you want to delete?")):
        print("Launching search....")
        while handleSearch():
            pass
    ans = input("Enter List of Book id you want to delete (Eg. 20,39,12,14), q to quit: ") 
    if ans == "q" or ans == "Q":
        return()
    else:
        #ans = con.converter.escape(ans) # Thats why SQL is bad
        ans = con._cmysql.escape_string(ans).decode("utf-8")
        dataCursor.execute(f"select * from {config.mysql['table']} where Booknumber in ({ans})") 
        data = dataCursor.fetchall()
        data.insert(0,("Book ID","Name","Author","Price","Genre"))
        print("Rows to be deleted: ")
        print(tabulate(data,headers="firstrow",tablefmt="github"))
        print()
        if(ask("Are you sure You want to delete these Entries?")):
            dataCursor.execute(f"delete from {config.mysql['table']} where Booknumber in ({ans})") 
            con.commit()
            print("Deleted")
        else:
            print("Deletion Cancelled")

def PrintPages(sql,tpl):
    dataCursor.execute(sql,tpl)
    firstEntry = True
    while True:
        data = dataCursor.fetchmany(25)
        if(len(data)==0):
            if firstEntry:
                print("No Record Found Matching your query")
            else:
                print("End of Records")
            break
        if firstEntry:
            print(tabulate(data,tablefmt="github",headers=("Book ID","Name","Author","Price","Genre")))
            firstEntry = False
        else:
            print(tabulate(data,tablefmt="github"))
        res = input("(Enter,q): ")
        if(res=="q"):
            dataCursor.fetchall()
            return(False)
    return(True)

    
def handleSearch():
    print()
    dict = {
            "2":"Booktitle",
            "3":"Author",
            "4":"Genre"
        }
    print("Explore Database ")
    print("1. View All record")
    print("2. Search By Name")
    print("3. Search By Author")
    print("4. Search By genre")
    print("5. Search By Book Id")
    print("q. Go Back")
    while True:
        response = input("What would you like to do? (1,2,3,4,5,q): ")
        if(response == "q"):
            return(False)
        elif(response not in ["1","2","3","4","5"]):
            print("Invalid input!")
        else:
            break
    if(response=="1"):
        return PrintPages(f"SELECT * from {config.mysql['table']} ORDER BY Booktitle ASC ",None)
    elif(response=="5"):
        param = input("Enter Book Id: ")
        return PrintPages(f"SELECT * from {config.mysql['table']} Where Booknumber = %s ",(int(param),))
    else:
        param = input("Enter What to Search For: ")
        return PrintPages(f"SELECT * from {config.mysql['table']} Where LOWER ({dict[response]}) LIKE %s",(f"%{param.lower()}%",))


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
    print("1. Insert Records")
    print("2. Update Records")
    print("3. Delete Records")
    print("4. Search or Explore records")
    print("q. Quit")
    
    choice = input("What would you like to do? (1/2/3/4/q): ")
    try:
        if choice == "1":
            handleInsert()
        elif choice == "2":
            while handleUpdate():
                pass
        elif choice == "3":
            handleDelete()
        elif choice == "4":
            while handleSearch():
                pass
        elif choice == "q":
            break
        else:
            print("Invalid Input!!")
    except Exception as e:
        print(e)
        print("Sorry there was a error Processing your query, Please Try again")
con.close()

