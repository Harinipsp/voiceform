from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
import os
from werkzeug.security import generate_password_hash, check_password_hash
from googletrans import Translator

# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Translator for multilingual support
translator = Translator()


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="r@m4112004",
        database="insurancedb"
    )

# Home route
@app.route('/')
def home():
    return redirect('/signup')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return submit_signup()
    return render_template('signup-btn.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return submit_login()
    return render_template('login-btn.html')

# Signup submission route
@app.route('/submit_signup', methods=['POST'])
def submit_signup():
    try:
        first_name = request.form['firstName']
        middle_name = request.form.get('middleName', '')
        last_name = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        query = """
        INSERT INTO Users (firstName, middleName, lastName, email, password)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (first_name, middle_name, last_name, email, hashed_password)
        with get_db_connection() as db:
            with db.cursor() as cursor:
                cursor.execute(query, values)
                db.commit()
        flash("Signup successful! Please log in.", "success")
        return redirect('/login')
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash("There was an error during signup. Please try again.", "error")
        return redirect('/signup')

# Login submission route
# Login submission route
@app.route('/submit_login', methods=['POST'])
def submit_login():
    email = request.form['email']
    password = request.form['password']
    try:
        query = "SELECT * FROM Users WHERE email = %s"
        with get_db_connection() as db:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute(query, (email,))
                user = cursor.fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['first_name'] = user['firstName']  # Store first name in session
            session['middle_name'] = user['middleName']  # Store middle name in session
            session['last_name'] = user['lastName']  # Store last name in session
            flash("Login successful!", "success")
            print("Session Variables:", session)
            return redirect('/form-filling')
        else:
            flash("Invalid credentials. Please try again.", "error")
            return redirect('/login')
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        flash("There was an error during login. Please try again.", "error")
        return redirect('/login')

# Form filling route
@app.route('/form-filling', methods=['GET', 'POST'])
def form_filling():
    if 'user_id' not in session:
        flash("Please log in to access the Medical Insurance Form.", "warning")
        return redirect('/login')
    # Retrieve user details from session
    first_name = session.get('first_name', '')
    middle_name = session.get('middle_name', '')
    last_name = session.get('last_name', '')
    email = session.get('email', '')

    if request.method == 'POST':
        try:
            # Collecting form data
            first_name = request.form['firstName']
            middle_name = request.form.get('middleName', '')
            last_name = request.form['lastName']
            gender = request.form.get('gender', 'not specified')
            age = request.form['age']  # Collect age
            status = request.form.get('status', 'not specified')  # Collect status
            dob = request.form['dob']
            email = request.form['email']
            street_address = request.form['streetAddress']
            city = request.form['city']
            state_province = request.form['stateProvince']
            zip_code = request.form['zipCode']
            phone_number = request.form['phoneNumber']
            applicant_type = request.form.get('applicantType', '')
            applicant_full_name = request.form.get('applicantFullName', '')
            applicant_gender = request.form.get('applicantGender', '')
            applicant_dob = request.form.get('applicantDob', '')
            

            # Insert into the database
            query = """
            INSERT INTO InsuranceForms (firstName, middleName, lastName, gender, age, status, dob, streetAddress, city, stateProvince, zipCode, email, phoneNumber, applicantType, applicantFullName, applicantGender, applicantDob)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (first_name, middle_name, last_name, gender, age, status, dob, street_address, city, state_province, zip_code, email, phone_number, applicant_type, applicant_full_name, applicant_gender, applicant_dob)

            # Debugging output
            print("Query:", query)
            print("Values:", values)

            with get_db_connection() as db:
                with db.cursor() as cursor:
                    cursor.execute(query, values)
                    db.commit()

            flash("Form submitted successfully!", "success")
            return redirect('/form-filling')
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            flash("There was an error while submitting the form. Please try again.", "error")
            return redirect('/form-filling')

    return render_template('index.html', first_name=first_name, middle_name=middle_name, last_name=last_name, email=email)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
