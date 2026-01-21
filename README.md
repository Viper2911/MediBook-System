# 🏥 MediBook - AI-Powered Telemedicine System

MediBook is a smart telemedicine platform that connects patients with the right doctors using **Machine Learning**. Unlike traditional booking apps, MediBook uses **Natural Language Processing (NLP)** to analyze patient symptoms and recommend the most suitable specialist automatically.

---

## 🚀 Key Features

### 🧠 AI Doctor Recommendation (ML Integration)
* **Symptom-Based Search:** Users describe their problem in plain English (e.g., *"I have severe chest pain and breathing issues"*).
* **TF-IDF & Cosine Similarity:** The system calculates the similarity between the user's symptoms and the doctor's expertise tags.
* **Smart Ranking:** Displays the top 5 relevant specialists with a "Match Score".

### 📅 Appointment Management
* **Doctor Dashboard:** View all upcoming patient appointments.
* **Patient Dashboard:** Track booking status (Confirmed/Pending).
* **Instant Booking:** One-click appointment scheduling.

### 🔐 Secure Authentication
* **Role-Based Login:** Separate views for **Patients** and **Doctors**.
* **Security:** Password hashing and session management using `Flask-Login`.

---

## 🛠️ Tech Stack

| Component | Technology Used |
| :--- | :--- |
| **Frontend** | HTML5, CSS3, Bootstrap 5 |
| **Backend** | Python, Flask |
| **Database** | SQLite (Lightweight & Fast) |
| **Machine Learning** | Scikit-Learn, Pandas, Joblib |
| **Algorithm** | TF-IDF Vectorization, Cosine Similarity |
| **Training Environment** | Kaggle Kernels (Offline Training) |

---

## 🏗️ System Architecture

The system follows a modular architecture where the ML model is trained offline and deployed for real-time inference.

1.  **Data Layer:** `doctors_dataset.csv` (Specialist data) & `database.db` (User/Appt data).
2.  **Training Layer:** Model trained on Kaggle -> Generates `.pkl` files (`vectorizer`, `matrix`, `dataframe`).
3.  **Application Layer:** Flask loads `.pkl` files -> Serves HTTP requests.

---

## ⚙️ Installation & Setup Guide

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/medibook.git](https://github.com/yourusername/medibook.git)
cd medibook
