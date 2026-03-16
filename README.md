# 🚀 Smart Task Manager

A modern productivity web application built with **Python Flask** that helps users manage tasks efficiently with AI-assisted features, analytics, and a drag-and-drop task board.

This project demonstrates full-stack development using backend APIs, authentication, UI dashboards, and productivity analytics.

---

# 📌 Features

### 🔐 User Authentication

* Secure **user registration and login**
* Password hashing using `werkzeug.security`
* Session-based authentication

### 📝 Task Management

* Create tasks with deadlines
* Delete tasks
* Mark tasks as completed
* Automatic **AI priority prediction**

### 🎤 Voice Task Input

* Add tasks using **speech recognition**
* Voice converts directly into task title

### 🧠 AI Priority Prediction

Tasks automatically get priority based on keywords.

Example:

* `exam`, `urgent`, `deadline` → **High priority**
* `study`, `project` → **Medium priority**
* Others → **Low priority**

### 📊 Productivity Analytics

Dashboard includes:

* Pending vs Completed tasks chart
* Weekly productivity insights

### 🧩 Drag & Drop Task Board

Kanban-style task board inspired by tools like Trello.

Columns:

* Pending
* Completed

Tasks can be moved visually for better workflow management.

### 🌙 Dark / Light Mode

Users can toggle UI themes for better readability.

### 🤖 Assistant Chatbot

Simple productivity assistant that helps users with:

* Task prioritization
* Productivity advice
* Work planning suggestions

---

# 🛠 Tech Stack

## Backend

* Python
* Flask
* SQLite

## Frontend

* HTML
* CSS
* JavaScript

## Libraries / Tools

* Chart.js (analytics graphs)
* SortableJS (drag & drop board)
* Web Speech API (voice input)

---

# 📂 Project Structure

```
smart-task-manager
│
├── app.py
├── database.db
├── requirements.txt
├── README.md
│
├── templates
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
│
└── static
```

---

# ⚙️ Installation

### 1️⃣ Clone Repository

```
git clone https://github.com/Girish0508-colab/smart-task-manager.git
cd smart-task-manager
```

### 2️⃣ Install Dependencies

```
pip install flask werkzeug
```

or

```
pip install -r requirements.txt
```

### 3️⃣ Run Application

```
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

# 📸 Application Screens

Main Dashboard Includes:

* Task creation
* Drag & Drop board
* Productivity chart
* AI assistant
* Dark/light theme toggle

---

# 🔮 Future Improvements

Possible upgrades for the project:

* Calendar-based task planning
* Email reminders
* Real AI integration using OpenAI API
* Mobile responsive UI
* Multi-user collaboration
* Task categories and tags
* Cloud database integration

---

# 📚 Learning Outcomes

This project demonstrates:

* Full stack web development
* REST-style backend routes
* Authentication systems
* Frontend interactivity with JavaScript
* Database integration
* Basic AI logic integration
* Data visualization

---

# 👨‍💻 Author

**Girish Kumar**

GitHub:
https://github.com/Girish0508-colab

---

# ⭐ Support

If you like this project:

* ⭐ Star the repository
* 🍴 Fork the project
* 🛠 Contribute improvements
