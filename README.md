# 💪 Muscle Fit Gym - Gym Management System

A comprehensive, role-based **Gym Management System** built with **Django** (Python), **Bootstrap 5**, and **SQLite**. This system caters to all operations of a modern gym, providing dedicated access portals and features for Administrators, Receptionists, Trainers, and Gym Members.

---

## 🌟 Key Features

### 🔐 Multi-Role Authentication & Portals
- **Administrator Dashboard**: System configuration, role management, dashboard analytics, system logs, reports access.
- **Receptionist Dashboard**: Member registrations, payment recordings, subscription plans management, daily attendance logs.
- **Trainer Dashboard**: Member assignments, personalized workout creation, customized diet planning.
- **Member Portal**: Personal profile management, subscription status tracking, diet & workout schedules, invoice/receipt downloads.

### 📅 Core Modules
- **Attendance Tracking**: Daily attendance logs, check-ins, history, and automated attendance analysis.
- **Membership Plans**: Management of flexible plans, subscription models, and billing cycles.
- **Diet & Workouts**: Custom exercise plans, daily workout routines, diet charts, and nutrition guidelines.
- **Billing & Payments**: Invoice logging, revenue analytics, auto-generated payment receipts (PDF).
- **Notifications System**: In-app notifications/alerts for payment reminders, announcements, and scheduling.
- **Automated Reporting**: Export tools for attendance logs, revenue sheets to **Excel** (`.xlsx`), and payment invoices to **PDF**.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.x, Django 5.1.x
- **Database**: SQLite (default, easily switchable to PostgreSQL or MySQL)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, Crispy Forms
- **Key Python Packages**:
  - `python-decouple` (environment variable management)
  - `openpyxl` (Excel report generation)
  - `reportlab` (PDF invoice generation)
  - `qrcode` (QR code generation for members/check-ins)
  - `pillow` (image processing for profile pictures)

---

## 🚀 Getting Started

### 📋 Prerequisites
Make sure you have Python (version 3.10+ recommended) and Git installed on your system.

### 🔧 Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Kumaran018/Gym-management-system-Django-.git
   cd Gym-management-system-Django-
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```
   *Activate it:*
   - **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
   - **Windows (CMD):** `.\venv\Scripts\activate.bat`
   - **macOS/Linux:** `source venv/bin/activate`

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and set your variables (e.g., customize `DJANGO_SECRET_KEY` if needed).

5. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Seed Initial Data (Optional):**
   Run the scratch scripts to populate the database with demo/test data:
   ```bash
   python scratch/seed_more_data.py
   python scratch/seed_notifications.py
   python scratch/seed_admin_notifications.py
   ```

7. **Create a Superuser (Admin):**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start the Development Server:**
   - Using the provided batch script (Windows only):
     ```cmd
     run_gym.bat
     ```
   - Or run standard django command:
     ```bash
     python manage.py runserver
     ```

9. Access the application in your browser at `http://127.0.0.1:8000/`.

---

## 📁 Project Structure

```text
Gym-management-system-Django/
├── apps/                 # Core applications of the project
│   ├── attendance/       # Attendance logs and management
│   ├── authentication/   # User accounts, login/register, decorators
│   ├── core/             # Base layouts, public pages, main views
│   ├── dashboard/        # Dashboards matching specific user roles
│   ├── diets/            # Diet plans and nutrition tracking
│   ├── members/          # Member profiles and details
│   ├── membership/       # Membership subscription plans
│   ├── notifications/    # Alert system
│   ├── payments/         # Billings, receipts, and invoices
│   ├── reports/          # Excel and PDF reporting tools
│   ├── trainers/         # Trainer assignments
│   └── workouts/         # Workout plans and exercises
├── gym_project/          # Project configuration (settings, URLs, WSGI)
├── static/               # CSS, JS, and global asset files
├── templates/            # HTML templates organized by modules
├── scratch/              # Database seed scripts
├── requirements.txt      # Project dependencies
└── run_gym.bat           # Server quick launch script
```
