import pytest 
from unittest.mock import MagicMock,patch
from Library import LibraryManagementSystem

def conn():
    db_conn=MagicMock()
    cursor=MagicMock()
    db_conn.cursor.return_value=cursor
    with patch('mysql.connector.connect', return_value=db_conn):
        # Create an instance of LibraryManagementSystem
        LMS = LibraryManagementSystem()
    return LMS,cursor,db_conn

def test_add_book():
    LMS,mock_cursor,mock_conn=conn()
    LMS.add_book('123-456-789','William','Othello',1622,5)
    query = "INSERT INTO books (ISBN,Author,Title,Year,Count) VALUES (%s, %s, %s, %s, %s)"
    mock_cursor.execute.assert_called_once_with(
        query,
        ('123-456-789','William','Othello',1622,5)
    )
    mock_conn.commit.assert_called_once()
