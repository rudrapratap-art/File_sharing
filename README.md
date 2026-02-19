# ☁️ Cloud File Sharing System

A cloud-based file sharing web application built using **Python Flask** and **Cloudinary**, with user authentication, admin control, and storage monitoring.

This project allows users to upload and view files online, while admins can manage and delete files.

---

## 🚀 Features

### 👤 User Features
- User Registration & Login
- Secure Password Hashing
- Upload Files (Login Required)
- View Uploaded Files (Public)
- Logout System

### 👑 Admin Features
- Admin Login
- View All Files
- Delete Any File
- Storage Usage Monitor

### 📊 System Features
- Cloud Storage (Cloudinary)
- Storage Usage Meter
- Mobile Responsive UI
- Public Homepage
- Secure Session Management

---

## 🛠️ Technologies Used

- Python
- Flask
- SQLite (User Database)
- Cloudinary API
- HTML5 / CSS3
- Gunicorn (Deployment)
- Render (Hosting)

---

## 📁 Project Structure

file_server/ │ ├── server.py ├── requirements.txt ├── README.md ├── .gitignore │ └── templates/ ├── index.html ├── admin.html ├── login.html ├── user_login.html └── register.html

---

## ⚙️ Installation (Local Setup)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Create .env File

Create a .env file in root directory:

CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
ADMIN_USER=admin
ADMIN_PASS=12345
SECRET_KEY=your_secret_key

4️⃣ Run Application

python server.py

Open in browser:

http://localhost:5000


---

🌐 Deployment on Render

Steps:

1. Upload project to GitHub


2. Create account on https://render.com


3. Create New Web Service


4. Connect GitHub repository


5. Set:



Build Command

pip install -r requirements.txt

Start Command

gunicorn server:app

6. Add Environment Variables on Render Dashboard


7. Deploy 🚀



You will get a live URL like:

https://your-app.onrender.com


---

🔐 Security

Passwords are hashed using Werkzeug

Admin credentials stored in environment variables

Sensitive files excluded using .gitignore

Session-based authentication



---

📊 Storage Monitoring

The system automatically tracks storage usage using:

Cloudinary Usage API

Manual fallback calculation


Displays:

Used Storage / Total Limit (%)


---

🧪 Test Accounts

Admin

Username: admin
Password: 12345

(Change in .env file)

User

Create your own account using Register page.


---

📈 Future Improvements

Per-user file storage

File sharing system

Download counter

PostgreSQL database

Android App

Dark Mode



---

👨‍💻 Developer

Rudra Pratap Kumar

Mechanical Engineering Student
Python & Web Development Enthusiast


---

📄 License

This project is developed for educational purposes.

You are free to use and modify it.

---

# 🎯 What This README Gives You

✔ Professional documentation  
✔ Clear installation steps  
✔ Deployment guide  
✔ Resume-ready project  
✔ Interview-friendly explanation  

---

## 🚀 Bonus Tip (Very Important)

GitHub pe upload karne se pehle:

.gitignore .env users.db

Check kar lena — secret leak na ho ❌

---

Agar chaho next:

👉 GitHub profile optimize karein  
👉 Resume project section likhein  
👉 Project demo video script banayein  

Bolo kya chahiye 😎💪