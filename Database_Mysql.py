import mysql.connector

def main():

    cnx = mysql.connector.connect(user='root', password='Zyk19960109',
                                  host='localhost',
                                  database='Warehouse_228')
    cnx.close()



main()