import mysql.connector

class LibraryManagementSystem:
    def __init__(self):
        self.host='localhost'
        self.username='root'
        self.password='root'
        self.database=""

        self.conn=mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database

        )
    
    def add_book(self,ISBN,Author,Title,Year,Count):
        cursor=self.conn.cursor()
        query="INSERT INTO books (ISBN,Author,Title,Year,Count) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query,(ISBN,Author,Title,Year,Count))
        self.conn.commit()
        cursor.close()