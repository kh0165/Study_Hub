# Study Hub 📚

Study Hub is a web application designed to help students organize and manage their academic life in one place.

## ✨ Features

- User Registration and Login
- User Profile Management
- Password Change
- Forgot Password & Password Reset via Email
- Dashboard
- Subject Management
- Notes Management
- Note Categories
- Course Management
- Tasks Management
- Assignments Management
- Study Resources Management
- Progress Tracking
- Analysis and History
- Search Functionality
- AI Chatbot
- Responsive User Interface

## 🛠️ Technologies Used

### Backend
- Python
- Django

### Frontend
- HTML5
- CSS3
- JavaScript

### Database
- PostgreSQL

### Other Tools
- Git
- GitHub
- Gmail SMTP

## 📂 Project Structure

\`\`\`text
study-hub/
│
├── accounts/          # Authentication and user accounts
├── analysis/          # Study analysis features
├── chatbot/           # AI chatbot functionality
├── config/            # Django project configuration
├── dashboard/         # Dashboard functionality
├── study/             # Subjects, notes, courses, tasks, assignments
├── static/            # CSS and JavaScript files
├── templates/         # HTML templates
├── manage.py
├── requirements.txt
├── .gitignore
├── .env               # Environment variables (not uploaded to GitHub)
└── README.md
\`\`\`

## ⚙️ Installation

### 1. Clone the Repository

\`\`\`bash
git clone https://github.com/kh0165/Study_Hub.git
cd Study_Hub
\`\`\`

### 2. Create a Virtual Environment

\`\`\`bash
python -m venv venv
\`\`\`

### 3. Activate the Virtual Environment

#### macOS / Linux

\`\`\`bash
source venv/bin/activate
\`\`\`

#### Windows

\`\`\`bash
venv\Scripts\activate
\`\`\`

### 4. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 5. Create a `.env` File

Create a `.env` file in the project root and add:

\`\`\`env
DB_NAME=final_project_db
DB_USER=postgres
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
\`\`\`

> ⚠️ Never upload your `.env` file to GitHub because it contains sensitive information.

### 6. Create the PostgreSQL Database

Create a PostgreSQL database named:

\`\`\`text
final_project_db
\`\`\`

### 7. Apply Migrations

\`\`\`bash
python manage.py migrate
\`\`\`

### 8. Run the Project

\`\`\`bash
python manage.py runserver
\`\`\`

Then open:

\`\`\`text
http://127.0.0.1:8000/
\`\`\`

## 📧 Password Reset

The project supports password reset via email using Gmail SMTP.

Users can:

1. Open the Forgot Password page.
2. Enter their registered email address.
3. Receive a password reset link.
4. Set a new password.
5. Log in with the new password.

For Gmail SMTP, use a Google App Password instead of your normal Gmail password.

## 🔐 Environment Variables

The project uses environment variables to keep sensitive information secure.

Example:

\`\`\`env
DB_NAME=final_project_db
DB_USER=postgres
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
\`\`\`

## 🚀 Git Workflow

After making changes:

\`\`\`bash
git add .
git commit -m "Describe your changes"
git push
\`\`\`