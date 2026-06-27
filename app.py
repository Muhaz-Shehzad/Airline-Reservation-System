from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_skylink_express'

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='F24-1009',  # Adjust based on your local MySQL root configurations
            database='airline_db'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    conn = get_db_connection()
    if conn is None:
        flash("Database server is currently offline. Please start MySQL.", "danger")
        return redirect('/')
        
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if user:
        session['user_id'] = user['user_id']
        session['name'] = user['name']
        session['role'] = user['role']
        flash(f"Welcome back, {user['name']}! Authentication successful.", "success")
        return redirect('/dashboard')
    else:
        flash("Invalid email credentials or password mismatch.", "danger")
        return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    conn = get_db_connection()
    if conn is None:
        flash("Database offline. Failed to sync dashboard records.", "danger")
        return redirect('/')
        
    cursor = conn.cursor(dictionary=True)
    
    # ROLE MANAGEMENT BOUNDARY CHECK
    if session.get('role') == 'admin':
        # Admin gets global master manifest rows
        query = """
            SELECT b.booking_id, b.seat_number, b.booking_date, s.flight_date, s.price, 
                   f.flight_number, f.departure_airport, f.arrival_airport, u.name as passenger_name
            FROM bookings b
            JOIN schedules s ON b.schedule_id = s.schedule_id
            JOIN flights f ON s.flight_number = f.flight_number
            JOIN users u ON b.user_id = u.user_id
            ORDER BY b.booking_date DESC
        """
        cursor.execute(query)
    else:
        # Standard passenger gets their specific tickets
        query = """
            SELECT b.booking_id, b.seat_number, b.booking_date, s.flight_date, s.price, 
                   f.flight_number, f.departure_airport, f.arrival_airport
            FROM bookings b
            JOIN schedules s ON b.schedule_id = s.schedule_id
            JOIN flights f ON s.flight_number = f.flight_number
            WHERE b.user_id = %s
            ORDER BY b.booking_date DESC
        """
        cursor.execute(query, (session['user_id'],))
        
    user_bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('dashboard.html', bookings=user_bookings)

@app.route('/search', methods=['GET'])
def search_flights():
    dep = request.args.get('departure')
    arr = request.args.get('arrival')
    date = request.args.get('date')
    
    conn = get_db_connection()
    if conn is None:
        return "Database link lost.", 500
        
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT s.schedule_id, s.flight_date, s.price, f.flight_number, 
               f.departure_airport, f.arrival_airport, f.departure_time, f.arrival_time
        FROM schedules s
        JOIN flights f ON s.flight_number = f.flight_number
        WHERE f.departure_airport = %s AND f.arrival_airport = %s AND s.flight_date = %s
    """
    cursor.execute(query, (dep, arr, date))
    available_flights = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('flights.html', flights=available_flights, search_params={'dep': dep, 'arr': arr, 'date': date})

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if session.get('role') != 'admin':
        flash("Unauthorized access denied.", "danger")
        return redirect('/')
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        flight_num = request.form.get('flight_number')
        aircraft_id = request.form.get('aircraft_id')
        f_date = request.form.get('flight_date')
        price = request.form.get('price')
        
        insert_query = "INSERT INTO schedules (flight_number, aircraft_id, flight_date, price) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (flight_num, aircraft_id, f_date, price))
        conn.commit()
        flash("New operational route run published successfully!", "success")
        
    cursor.execute("SELECT * FROM flights")
    all_flights = cursor.fetchall()
    
    cursor.execute("SELECT s.*, f.departure_airport, f.arrival_airport FROM schedules s JOIN flights f ON s.flight_number = f.flight_number ORDER BY s.flight_date DESC")
    all_schedules = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('admin.html', flights=all_flights, schedules=all_schedules)

@app.route('/logout')
def logout():
    session.clear()
    flash("Session signed out securely. Goodbye!", "info")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)