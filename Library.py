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
    def book_borrow(self,ISBN):
        cursor = self.conn.cursor()
        query = "SELECT Count FROM books WHERE ISBN = %s"
        cursor.execute(query, (ISBN,))
        result = cursor.fetchone()
        if result and result[0] > 0:
            # Update the count 
            update_query = "UPDATE books SET Count = Count - 1 WHERE ISBN = %s"
            cursor.execute(update_query, (ISBN,))
            self.conn.commit()
            cursor.close()
            return True
        else:
            cursor.close()
            raise ValueError("Book is not available")
    def view_books(self):
        cursor=self.conn.cursor()
        query="SELECT * FROM books WHERE Count > 0"
        cursor.execute(query)
        results=cursor.fetchall()
        books=[]
        for row in results:
            books.append({
                'ISBN':row[0],
                'Author':row[1],
                'Title':row[2],
                'Year':row[3],
                'Count':row[4]
            })
        return books
    def return_book(self, ISBN):
        cursor = self.conn.cursor()
        query = "SELECT Count FROM books WHERE ISBN = %s"
        cursor.execute(query, (ISBN,))
        result = cursor.fetchone()
        if result:
            update_query = "UPDATE books SET Count = Count + 1 WHERE ISBN = %s"
            cursor.execute(update_query, (ISBN,))
            self.conn.commit()
        else:
            raise ValueError("Book not found")
        cursor.close()

