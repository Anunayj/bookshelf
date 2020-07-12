import config
import mysql.connector
import sys
try:
    con = mysql.connector.connect(
        host=config.mysql["host"],
        port=3306,
        user=config.mysql["user"],
        password=config.mysql["password"],
        database=config.mysql["database"])
except:
    print("There was a error connecting to the servers");
    sys.exit(1)
print("Connection Successful")



