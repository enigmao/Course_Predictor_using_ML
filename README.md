# Credit Health Check - Flask + Google Sheets

This project is a **Flask web application** that collects responses to 20 credit health questions, predicts a risk category, and stores submissions in a **Google Spreadsheet**.

---

## 🚀 Features
- Flask-based questionnaire with **20 Yes/No questions**.
- Collects **Name, Email, and answers**.
- Predicts a **remedy status** (0: Preventive, 1: Remedy Needed, 2: Urgent, n/a: Invalid).
- Saves responses with **date, name, email, answers, prediction** to a Google Sheet.

---

## 🛠 Requirements

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

**requirements.txt**
```
Flask==3.0.3
gunicorn==22.0.0
numpy==1.26.4
joblib==1.4.2
Werkzeug==3.0.3
gspread==6.1.2
google-auth==2.34.0
flask-limiter==3.7.0   # optional, for rate limiting
```

---

## 🔑 Setup Google Sheets API

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Google Sheets API**.
3. Create a **Service Account**, download the JSON credentials.
4. Share your Google Sheet with the service account email.
5. Store credentials securely using **environment variables**:

```bash
export GOOGLE_SA_JSON='{"type":"service_account",...}'   # full JSON content as string
export SHEET_ID='your_google_sheet_id_here'
```

---

## ▶️ Running the App

### Local development
```bash
python Application.py
```
Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Production (recommended with Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 Application:app
```

Deploy behind **Nginx or AWS ALB** with HTTPS enabled.

---

## 📊 Data Saved in Google Sheets

| Date       | Name | Email | Q1 | Q2 | ... | Q20 | Prediction |
|------------|------|-------|----|----|-----|-----|------------|
| 2025-09-03 | John Doe | john@example.com | 1 | 0 | ... | 1 | 2 |

- `1` = Yes, `0` = No
- `Prediction` values:
  - `0` → Take preventive action
  - `1` → Need remedy
  - `2` → Urgently needed
  - `n/a` → Invalid input

---

## 🔒 Security Notes
- Do **not commit** your `credentials.json` file to GitHub.
- Use **environment variables** or AWS SSM/Secrets Manager.
- Always run Flask in **production mode** behind Gunicorn/Nginx.
- Restrict **SSH** and allow only HTTPS/HTTP(S) inbound traffic on EC2.

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

## 📌 Next Steps
- Add more analytics or visualizations in Google Sheets.
- Extend the ML model (`RemedyModel.pkl`) for more accurate predictions.
- Harden EC2 security with **Nginx + HTTPS**.

---

✅ This app is ready to deploy on **AWS EC2** or any cloud server!
