import config
import mysql.connector
import sys




def setupTable(cursor):
    cursor.execute("SHOW TABLES LIKE %s",(config.mysql["table"],))
    result = cursor.fetchone()
    if result:
        print(f"Using table {config.mysql['table']}")
        pass
        #TODO: Check Correct Schema
    else:
        print("Table not Found, Setting up a new table")
        cursor.execute(f"CREATE TABLE {config.mysql['table']} (Booknumber int UNSIGNED PRIMARY KEY AUTO_INCREMENT,Booktitle varchar(255),Author varchar(255),Price int , Genre varchar(50))")


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

setupTable(dataCursor)




