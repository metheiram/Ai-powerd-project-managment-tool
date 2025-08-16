

# 🧠 Smart Project Management App

A Django-based Smart Project Management Tool designed to streamline project planning, task management, team collaboration, and overall productivity using AI-powered automation and clean user interfaces.

---

## 🚀 Features

- 📝 Project and Task Creation with due dates and statuses
- 🧑‍🤝‍🧑 Assign tasks to users with priorities and collaboration
- 📊 Visual task progress tracking (0–100%)
- ⚠️ Automatic overdue detection and task cleanup
- 📅 Start and Due Dates with filtering and search options
- 🔄 Real-time task status updates
- 📁 Admin and user dashboards
- 🧩 Modular code with separate apps for user, task,notification, data, project, and profile management

---



## 🛠️ Tech Stack

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, TailwindCSS,js
- **Database**: SQLite3 (default)
- **Other Tools**: VSCode, Git, Django Admin, Custom Forms
- **Libraries**: Django Forms, ModelForms, Bootstrap/Tailwind (if applicable)

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/metheiram/smart-project_managment_app-main.git
cd smart-project_managment_app-main
```

### 2. Set Up Virtual Environment
```bash
python -m venv myenv
Windows: myenv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (optional)
```bash
python manage.py createsuperuser
```

### 6. Run the Server
```bash
python manage.py runserver
```

---

## 🔧 Usage

- Visit `http://127.0.0.1:8000`
- Login/Register as a user
- Create projects, assign tasks, manage deadlines and priorities
- Use admin panel for global control

---

## 🔐 Environment Variables

Add a `.env` file in the root directory with the following format:

```env
SECRET_KEY=your-secret-key
DEBUG=True
EMAIL_HOST=your-email-host
EMAIL_PORT=your-port
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-password
```

---

## 📁 Directory Structure

```
smart-project_managment_app/
├── data/                   # Task and project logic
├── users/                  # Custom user and profile management
├── templates/              # HTML templates
├── static/                 # CSS, JS, and assets
├── media/                  # User-uploaded files
├── manage.py
├── .env                    # Environment variables
├── db.sqlite3              # SQLite database
```

---

## 👤 Author

**IRAM MUKHTAR**  
Built as a final year project with real-time collaboration features and automated task tracking.

---


## 📬 Contact

For questions, issues, or feature requests, please contact:  
📧 iamhinamukhtar@gmail.com

---

## 🗺️ Roadmap

- [x] Task and project assignment
- [x] User registration and profile setup
- [ ] Kanban board integration
- [ ] Notification 
- [ ] Multi-language support

---

## 🏷️ Badges

![Django](https://img.shields.io/badge/Made%20with-Django-blue)


---

## 🙏 Acknowledgments

- Django Documentation
- GitHub Open Source Projects
- Stack Overflow Community
