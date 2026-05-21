# 🐾 VetCare Wellness Portal (VetClinic)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Tkinter](https://img.shields.io/badge/UI-Tkinter-green?style=for-the-badge)
![SQL Server](https://img.shields.io/badge/Database-SQL%20Server-red?style=for-the-badge&logo=microsoftsqlserver)
![Status](https://img.shields.io/badge/Project-Veterinary%20Management-orange?style=for-the-badge)

### 🏥 Modern Veterinary Clinic Management System

A desktop application for managing veterinary clinics using **Python**, **Tkinter**, and **Microsoft SQL Server**.

</div>

---

# ✨ Features

## 📊 Dashboard

- Real-time statistics overview
- Upcoming visits tracking
- Vaccine booster reminders
- Quick clinic insights

---

## 🛠 CRUD Management

Manage all major entities:

- 👤 Owners
- 🐶 Pets
- 🏥 Clinics
- 👨‍⚕️ Veterinarians
- 📅 Visits
- 💉 Vaccines
- 📝 Vaccination Records
- 📄 Clinical Notes
- 🔗 Works At Relationships

---

## 📈 Reports & Analytics

Built-in SQL reports:

| Report | Description |
|---|---|
| 🐾 Most Visited Species | Most visited pet species |
| 🏥 Clinics With No Visits | Detect inactive clinics |
| 💉 Top Vaccinating Vet | Highest vaccination activity |
| 👤 Owners Without Visits | Inactive owners |
| 📊 Vaccines Per Clinic | Clinic vaccine statistics |
| 📅 Visits Per Pet | Yearly visit analytics |

---

## 🌗 UI Features

- Dark Mode
- Light Mode
- Modern sidebar navigation
- Responsive desktop layout

---

## 🤖 Gemini AI Chat

Integrated AI chatbot powered by Gemini API.

Features:
- AI-powered assistance
- Configurable model support
- Lightweight implementation using `urllib`

---

# 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core Application |
| Tkinter | GUI Framework |
| SQL Server | Database |
| pyodbc | Database Connectivity |
| urllib | Gemini API Requests |

---

# 📋 Prerequisites

Before running the project, install:

- ✅ Python 3.10+
- ✅ Microsoft SQL Server
- ✅ ODBC Driver 17 for SQL Server
- ✅ Windows OS (recommended)

---

# ⚙️ Setup Guide

## 1️⃣ Create Database Schema

Run the SQL file:

```powershell
sqlcmd -S localhost -E -i .\final.sql
```

### Notes

- Creates the `VetClinic` database automatically
- Recreates all tables and constraints

---

## 2️⃣ Setup Python Environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pyodbc
```

---

## 3️⃣ Run the Application

```powershell
python .\VetClinic\main.py
```

---

# 🤖 Gemini AI Configuration

1. Open the application
2. Go to **Settings**
3. Paste your Gemini API key
4. Save settings
5. Open the **AI Chat** screen

> API keys are stored locally in:
>
> `VetClinic/user_settings.json`

---

# 🗄 Database Configuration

Default settings:

| Setting | Value |
|---|---|
| Server | localhost |
| Database | VetClinic |
| Authentication | Trusted Connection |
| Driver | ODBC Driver 17 |

Configuration file:

```python
VetClinic/db_connection.py
```

---

# 🧱 Database Schema

## Core Tables

| Table | Description |
|---|---|
| OWNER | Owner information |
| PET | Pet records |
| CLINIC | Clinic locations |
| VETERINARIIAN | Veterinarian data |
| WORKSAT | Vet-clinic relationships |
| VIST | Visits records |
| CLINICAL_NOTE | Medical notes |
| VACCINE | Vaccine catalog |
| VACCINATIONRECORD | Vaccination history |

> ⚠️ Note:
>
> The visits table is named `VIST` instead of `VISIT`.

---

# 📂 Project Structure

```bash
VetClinic/
│
├── main.py
├── db_connection.py
├── screens/
├── queries/
├── services/
│
└── final.sql
```

---

# 🧪 Troubleshooting

## pyodbc Installation Issues

```powershell
python -m pip install -U pip
```

You may also need Microsoft Visual C++ Build Tools.

---

## ODBC Driver Not Found

Install:
- ODBC Driver 17 for SQL Server
- OR update the driver name inside:

```python
VetClinic/db_connection.py
```

---

## Database Connection Errors

Verify:

- SQL Server is running
- `VetClinic` database exists
- Your server name matches the configuration

---

# 🚀 Future Improvements

- 🌐 Web version
- 📱 Mobile support
- 📊 Advanced analytics dashboard
- 🔔 Notifications system
- ☁️ Cloud deployment

---

# 👨‍💻 Authors

Developed as a veterinary clinic management system project using Python, Tkinter, and Microsoft SQL Server.

---

<div align="center">

## ⭐ If you like this project, consider starring the repository!

</div>

