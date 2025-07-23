from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import uuid

app = Flask(__name__)

# Create the bookings table if it doesn't exist
with sqlite3.connect("tickets.db") as conn:
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id TEXT PRIMARY KEY,
            name TEXT,
            date TEXT,
            time TEXT,
            persons INTEGER,
            amount TEXT
        )
    ''')
    conn.commit()

# Home / Welcome Page
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Booking Form Page
@app.route('/book', methods=['GET', 'POST'])
def book_ticket():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        persons = int(request.form['persons'])
        amount = request.form['amount']

        # Generate a unique booking ID
        booking_id = str(uuid.uuid4())[:8]

        # Save booking to DB
        with sqlite3.connect("tickets.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO bookings (id, name, date, time, persons, amount) VALUES (?, ?, ?, ?, ?, ?)",
                      (booking_id, name, date, time, persons, amount))
            conn.commit()

        # Pass booking details to thank you page
        return render_template('thankyou.html', booking_id=booking_id, name=name, date=date, time=time, persons=persons, amount=amount)

    return render_template('book_ticket.html')

# Booking History Page
@app.route('/history')
def history():
    with sqlite3.connect("tickets.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM bookings ORDER BY rowid DESC")
        bookings = c.fetchall()
    return render_template('history.html', bookings=bookings)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
