from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector # Database connection logic [2]

app = Flask(__name__)
app.secret_key = 'secret_library_key'

# MySQL Connection Configuration [2]
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # Update with your MySQL username
        password="111", # Update with your MySQL password
        database="library_db"
    )

# 1. Homepage / Dashboard [1]
@app.route('/')
def index():
    return render_template('index.html')

# 2. View all books [1]
@app.route('/books')
def list_books():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('list_books.html', books=books)

# 3. Add new book [1]
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title, author = request.form['title'], request.form['author']
        genre, qty = request.form['genre'], request.form['qty']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, genre, qty) VALUES (%s, %s, %s, %s)", 
                       (title, author, genre, qty))
        conn.commit()
        conn.close()
        return redirect(url_for('list_books'))
    return render_template('add_book.html')

# 4. Update book details [1]
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        title, author = request.form['title'], request.form['author']
        cursor.execute("UPDATE books SET title=%s, author=%s WHERE id=%s", (title, author, id))
        conn.commit()
        return redirect(url_for('list_books'))
    cursor.execute("SELECT * FROM books WHERE id=%s", (id,))
    book = cursor.fetchone()
    conn.close()
    return render_template('edit_book.html', book=book)

# 5. Delete a book [1]
@app.route('/delete/<int:id>')
def delete_book(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('list_books'))

# 6. Issue book to user [1]
@app.route('/issue', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST':
        book_id, user_id = request.form['book_id'], request.form['user_id']
        issue_date, return_date = request.form['issue_date'], request.form['return_date']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO issued_books (book_id, user_id, issue_date, return_date) VALUES (%s, %s, %s, %s)",
                       (book_id, user_id, issue_date, return_date))
        conn.commit()
        conn.close()
        return redirect(url_for('view_issued'))
    return render_template('issue_book.html')

# 7. View issued books [1]
@app.route('/issued')
def view_issued():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT i.id, b.title, u.name, i.issue_date, i.return_date 
        FROM issued_books i 
        JOIN books b ON i.book_id = b.id 
        JOIN users u ON i.user_id = u.id
    """)
    issued = cursor.fetchall()
    conn.close()
    return render_template('issued_books.html', issued=issued)

# 8. Return book [1]
@app.route('/return/<int:id>')
def return_book(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM issued_books WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_issued'))

if __name__ == '__main__':
    app.run(debug=True) # Starting Flask server [3]
