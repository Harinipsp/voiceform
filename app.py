from flask import Flask, render_template, request, redirect, flash, session
import os
# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(24)

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
        password = request.form['password']  # Password is collected but not stored

        # Store user info in session
        session['first_name'] = first_name
        session['middle_name'] = middle_name
        session['last_name'] = last_name
        session['email'] = email

        flash("Signup successful! Please log in.", "success")
        return redirect('/form-filling')
    except Exception as e:
        print(f"Unexpected Error: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect('/signup')

# Login submission route
@app.route('/submit_login', methods=['POST'])
def submit_login():
    email = request.form['email']
    password = request.form['password']
    # For simplicity, we are not validating login credentials
    session['email'] = email  # Store email in session
    flash("Login successful!", "success")
    return redirect('/form-filling')

# Form filling route
@app.route('/form-filling', methods=['GET', 'POST'])
def form_filling():
    if request.method == 'POST':
        return submit_form()  # Call the function to handle the form submission
    
    return render_template('index.html')  # Render the form-filling template

@app.route('/submit', methods=['POST'])
def submit_form():
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

    # Store collected info in session
    session['form_data'] = {
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'gender': gender,
        'age': age,
        'status': status,
        'dob': dob,
        'email': email,
        'street_address': street_address,
        'city': city,
        'state_province': state_province,
        'zip_code': zip_code,
        'phone_number': phone_number,
        'applicant_type': applicant_type,
        'applicant_full_name': applicant_full_name,
        'applicant_gender': applicant_gender,
        'applicant_dob': applicant_dob
    }

    flash("Form submitted successfully!", "success")
    return redirect('/display')

@app.route('/display')
def display():
    form_data = session.get('form_data', {})
    return render_template('display.html', form_data=form_data)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
