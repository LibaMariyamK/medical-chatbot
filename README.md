# Health Chatbot with Authentication

A web-based AI chatbot with user authentication that collects and stores medical information.

![Chatbot UI](C:\Projects\bot\static\images\Screenshot 2025-04-07 163050.png)

## Setup Instructions
1. Install Python 3.x.
2. Install dependencies: `pip install flask werkzeug`.
3. Run the application: `python app.py`.
4. Open `http://127.0.0.1:5000` in your browser.
5. Signup with an email and password, then login to use the chatbot.

## Approach
- **Frontend**: HTML/CSS/JS with signup/login forms and a chat interface.
- **Backend**: Flask with Python for authentication and chatbot logic.
- **Database**: SQLite with `users` (email, password) and `health_data` tables.
- **Features**: 
  - User signup/login/logout with password hashing.
  - Collects name, age, height, weight, blood group, calculates BMI, and records symptoms with feedback.
  - Data linked to user ID.

## Notes
- Input validation ensures realistic data.
- BMI feedback adds interactivity.
- Authentication restricts chatbot access to logged-in users.
