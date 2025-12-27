from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secret_library_key'

# MySQL Connection Configuration [1, 2]
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # Updated per source setup [1, 2]
        password="111",     # Updated per source setup [1, 2]
        database="library_db"
    )

# 1. Dashboard - Named 'index' to resolve BuildError in lili.PNG [2-4]
@app.route('/')
def index():
    return render_template('index.html')

# 2. Registration Logic - Uses 'user_name' to prevent IntegrityErrors [5-7]
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['user_name'] # Resolves KeyError in erroe.PNG [7, 8]
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Registering users first allows them to borrow books later [6, 7]
            cursor.execute("INSERT INTO users (user_name, email, password) VALUES (%s, %s, %s)",
                           (user_name, email, password))
            conn.commit()
            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            return f"Error: {err}. Please use a unique Username."
        finally:
            conn.close()
    return render_template('register.html')

# 3. View Inventory [9, 10]
@app.route('/books')
def list_books():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return render_template('list_books.html', books=books)

# 4. Add New Book - Named 'add_book' to resolve BuildError in ab.PNG [11, 12]
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        qty = request.form['qty']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, genre, qty) VALUES (%s, %s, %s, %s)",
                       (title, author, genre, qty))
        conn.commit()
        conn.close()
        return redirect(url_for('list_books'))
    return render_template('add_book.html')

# 5. Update Book - Named 'edit_book' and accepts 'id' to fix wi.PNG [13, 14]
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        title, author = request.form['title'], request.form['author']
        cursor.execute("UPDATE books SET title=%s, author=%s WHERE id=%s", (title, author, id))
        conn.commit()
        conn.close()
        return redirect(url_for('list_books'))
    
    cursor.execute("SELECT * FROM books WHERE id=%s", (id,))
    book = cursor.fetchone()
    conn.close()
    return render_template('edit_book.html', book=book)

# 6. Issue Book - Uses 'user_name' to match the database Foreign Key [5, 15, 16]
@app.route('/issue', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        user_name = request.form['user_name'] # Matches input in doct1.docx [15-17]
        issue_date = request.form['issue_date']
        return_date = request.form['return_date']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Ensures user exists in users table before issuing [5, 15, 16]
            cursor.execute("INSERT INTO issued_books (book_id, user_name, issue_date, return_date) VALUES (%s, %s, %s, %s)",
                           (book_id, user_name, issue_date, return_date))
            conn.commit()
            return redirect(url_for('view_issued'))
        except mysql.connector.Error as err:
            return f"Database Error: {err}. Ensure the User Name is registered first."
        finally:
            conn.close()
    return render_template('issue_book.html')

# 7. View Issued Ledger [18, 19]
@app.route('/issued')
def view_issued():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # The query below explicitly fetches 'user_name'
    cursor.execute("""
        SELECT i.id, b.title, i.user_name, i.issue_date, i.return_date
        FROM issued_books i
        JOIN books b ON i.book_id = b.id
    """)
    issued = cursor.fetchall()
    conn.close()
    # 'issued' list is sent to the template here
    return render_template('issued_books.html', issued=issued)
# 8. Return Page - Named 'return_book_page' to resolve BuildError in y.PNG [22, 23]
@app.route('/return_page')
def return_book_page():
    return render_template('return_book.html')

# 9. Return Logic - Handles the POST request from the manual return form [24]
@app.route('/return_logic', methods=['POST'])
def return_book_logic():
    book_id = request.form['book_id']
    user_name = request.form['user_name'] # This retrieves the Username you entered
    conn = get_db_connection()
    cursor = conn.cursor()
    # Deletes the record where the Book ID and Username both match
    cursor.execute("DELETE FROM issued_books WHERE book_id=%s AND user_name=%s", 
                   (book_id, user_name))
    conn.commit()
    conn.close()
    return redirect(url_for('view_issued'))

# 10. Direct Return - Used for return links within the ledger table [20, 21]
@app.route('/return/<int:id>')
def return_book(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM issued_books WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_issued'))
#Delete a Book [10]
# This route targets a specific book by ID to remove it from the database.
@app.route('/delete/<int:id>')
def delete_book(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Cascading ensures issued records for this book are also removed [1]
    cursor.execute("DELETE FROM books WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('list_books'))

if __name__ == '__main__':
    # Starting Flask server with debug mode enabled [26, 27]
    app.run(debug=True)