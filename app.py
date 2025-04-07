from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from database import init_db, save_user, authenticate_user, save_health_data, get_health_data
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure random key in production

# Initialize database
init_db()

# Home route - redirect to login if not authenticated
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            save_user(email, hashed_password)
            return redirect(url_for('login'))
        except Exception as e:
            return f"Signup failed: {str(e)}"
    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = authenticate_user(email)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        return "Invalid credentials"
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Chat endpoint - only for logged-in users
@app.route('/chat', methods=['POST'])
def chat():
    if 'user_id' not in session:
        return jsonify({'response': 'Please log in to use the chatbot.'}), 403

    user_input = request.json.get('message').lower().strip()
    user_session = request.json.get('session', {})

    if not user_session:
        user_session = {
            'step': 'start',
            'data': {'timestamp': datetime.datetime.now().isoformat(), 'user_id': session['user_id']}
        }

    response = ""
    next_step = user_session['step']

    if user_session['step'] == 'start':
        response = "Hello! Let's start with your name. What's your name?"
        next_step = 'name'

    elif user_session['step'] == 'name':
        user_session['data']['name'] = user_input
        response = f"Nice to meet you, {user_input}! How old are you?"
        next_step = 'age'

    elif user_session['step'] == 'age':
        try:
            age = int(user_input)
            if 1 <= age <= 120:
                user_session['data']['age'] = age
                response = "Great! What's your height in centimeters (e.g., 170)?"
                next_step = 'height'
            else:
                response = "Please enter a valid age between 1 and 120."
        except ValueError:
            response = "Please enter a number for your age."

    elif user_session['step'] == 'height':
        try:
            height = float(user_input)
            if 50 <= height <= 250:
                user_session['data']['height'] = height
                response = "Got it! What's your weight in kilograms (e.g., 70)?"
                next_step = 'weight'
            else:
                response = "Please enter a valid height between 50 and 250 cm."
        except ValueError:
            response = "Please enter a number for your height."

    elif user_session['step'] == 'weight':
        try:
            weight = float(user_input)
            if 20 <= weight <= 300:
                user_session['data']['weight'] = weight
                bmi = weight / ((user_session['data']['height'] / 100) ** 2)
                user_session['data']['bmi'] = round(bmi, 2)
                response = f"Your BMI is {user_session['data']['bmi']}. What's your blood group (e.g., A+, O-)?"
                next_step = 'blood_group'
            else:
                response = "Please enter a valid weight between 20 and 300 kg."
        except ValueError:
            response = "Please enter a number for your weight."

    elif user_session['step'] == 'blood_group':
        valid_groups = ['a+', 'a-', 'b+', 'b-', 'ab+', 'ab-', 'o+', 'o-']
        if user_input in valid_groups:
            user_session['data']['blood_group'] = user_input
            response = "Thanks! Do you have any current symptoms or health goals? (e.g., 'feeling tired', 'want to lose weight')"
            next_step = 'symptoms'
        else:
            response = "Please enter a valid blood group (e.g., A+, O-)."

    elif user_session['step'] == 'symptoms':
        user_session['data']['symptoms'] = user_input
        bmi = user_session['data']['bmi']
        bmi_feedback = (
            "You're underweight. Consider a balanced diet." if bmi < 18.5 else
            "Your weight is normal. Keep it up!" if 18.5 <= bmi < 25 else
            "You're overweight. Try regular exercise!" if 25 <= bmi < 30 else
            "Obese range. A health check-up is recommended."
        )
        response = f"Got it: '{user_input}'. BMI feedback: {bmi_feedback}. Saved your info. Type 'view' to see it or 'restart' to start over."
        save_health_data(user_session['data'])
        next_step = 'end'

    elif user_session['step'] == 'end':
        if user_input == 'view':
            data = get_health_data(session['user_id'])
            response = f"Here's your latest data: {data}"
        elif user_input == 'restart':
            user_session = {'step': 'start', 'data': {'user_id': session['user_id']}}
            response = "Let's start again. What's your name?"
            next_step = 'start'
        else:
            response = "Type 'view' to see your data or 'restart' to begin again."

    user_session['step'] = next_step
    return jsonify({'response': response, 'session': user_session})

if __name__ == '__main__':
    app.run(debug=True)