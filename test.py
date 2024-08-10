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

def test_borrow_success(): #Test case that successful borrow of available book
    LMS,mock_cursor,mock_conn=conn()
    mock_cursor.fetchone.return_value = (5,)
    result = LMS.book_borrow('123-456-789')
    mock_cursor.execute.assert_any_call(
        "SELECT Count FROM books WHERE ISBN = %s", ('123-456-789',)
    )
    mock_cursor.execute.assert_any_call(
        "UPDATE books SET Count = Count - 1 WHERE ISBN = %s", ('123-456-789',)
    )
    mock_conn.commit.assert_called_once()
    assert result is True
def test_borrow_failure():
    LMS,mock_cursor,mock_conn=conn()
    mock_cursor.fetchone.return_value = (0,)
    result=LMS.book_borrow('123-456-789')
    with pytest.raises(ValueError, match="Book is not available"):
        LMS.book_borrow('123-456-789')
    
    # Verify that the correct SQL commands were executed
    mock_cursor.execute.assert_any_call(
        "SELECT Count FROM books WHERE ISBN = %s", ('123-456-789',)
    )
    
    # Ensure no update was attempted or committed
    mock_cursor.execute.assert_not_called_with(
        "UPDATE books SET Count = Count - 1 WHERE ISBN = %s", ('123-456-789',)
    )
    mock_conn.commit.assert_not_called()
    assert result is False
def test_view_books():
    LMS,mock_cursor,_=conn()
    mock_cursor.fetchall.return_value = [
        ('123-456-789', 'William', 'Othello', 1622, 5)]
    expected_books = [
        {'ISBN': '123-456-789', 'Author': 'William', 'Title': 'Othello', 'Year': 1622, 'Count': 5}
           ]
    result = LMS.view_books()
    assert result == expected_books
    # Verify the database interaction
    mock_cursor.execute.assert_called_once_with("SELECT * FROM books WHERE Count > 0")
    