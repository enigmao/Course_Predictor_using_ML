# Credit Health Check - Flask + Google Sheets

This project is a **Flask web application** that collects responses to 20 credit health questions, predicts a risk category, and stores submissions directly in a **Google Spreadsheet**.

---

## 🚀 Features
- Flask-based questionnaire with **Yes/No questions**.
- Collects **Name, Email, and answers**.
- Predicts a **remedy status** (Preventive, Remedy Needed, Urgent, Invalid).
- Saves responses directly with **date, name, email, answers, prediction** to a Google Sheet.

---

## 🛠 Requirements

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

### Local development
```bash
python Application.py
```
Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Production 
```bash
gunicorn -w 4 -b 0.0.0.0:5000 Application:app
```

---

## 📊 Data Saved in Google Sheets

| Date       | Name | Email | Q1 | Q2 | ... | Q20 | Prediction |
|------------|------|-------|----|----|-----|-----|------------|
| 2025-08-03 | Your Name | you@example.com | Yes | No | ... | Yes | Urgent |

---

## 📂 Project Structure

```
.
├── Application.py     # Flask backend
├── index.html         # Questionnaire form
├── response.html      # Result page
├── requirements.txt   # Dependencies
└── README.md          # Project guide
```

---
