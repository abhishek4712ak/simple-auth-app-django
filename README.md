# Django Authentication App

A secure Django-based authentication system that provides user registration, login, logout, OTP verification, profile management, and password management features.

## 🚀 Features

* User Registration
* User Login & Logout
* OTP Verification
* Protected Dashboard
* Update Username
* Update Email Address
* Change Password
* Session-Based Authentication
* Responsive User Interface
* SQLite Database Support

## 📂 Project Structure

```text
simple-auth-app-django-main/
│
├── AuthApp/               # Django project settings
├── authapp/               # Main application
├── templates/             # HTML templates
├── static/                # CSS and static files
├── db.sqlite3             # SQLite database
└── manage.py
```

## 🛠️ Technologies Used

* Python 3
* Django
* HTML5
* CSS3
* SQLite

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/simple-auth-app-django.git
cd simple-auth-app-django
```

### 2. Create a Virtual Environment

```bash
python -m venv myenv
```

### 3. Activate Virtual Environment

#### Windows

```bash
myenv\Scripts\activate
```

#### Linux / macOS

```bash
source myenv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

If a requirements file is not available:

```bash
pip install django
```

## 🗄️ Database Setup

Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create an admin user (optional):

```bash
python manage.py createsuperuser
```

## ▶️ Run the Project

Start the development server:

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

## 📌 Available Routes

| Route             | Description        |
| ----------------- | ------------------ |
| /login/           | User Login         |
| /register/        | User Registration  |
| /verify-otp/      | OTP Verification   |
| /dashboard/       | User Dashboard     |
| /update-username/ | Update Username    |
| /update-email/    | Update Email       |
| /change-password/ | Change Password    |
| /logout/          | Logout User        |
| /admin/           | Django Admin Panel |

## 🔒 Authentication Flow

1. User registers an account.
2. OTP is generated and verified.
3. User logs in successfully.
4. User gains access to the protected dashboard.
5. User can update profile information or change password.
6. User can securely logout.

## 🌐 Deployment

This project can be deployed on:

* PythonAnywhere
* Render
* Railway
* Heroku
* VPS Servers

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

## 📄 License

This project is open-source and available under the MIT License.

## 👨‍💻 Author

Abhishek Kumar Kushwaha

If you found this project helpful, consider giving it a ⭐ on GitHub.
