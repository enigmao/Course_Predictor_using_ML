from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
import numpy as np
import joblib
import os
from werkzeug.middleware.proxy_fix import ProxyFix
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

MODEL_PATH = "RemedyModel.pkl"
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("RemedyData").sheet1  

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        
        name = request.form.get("name", "")
        email = request.form.get("email", "")

        user_input = []
        for i in range(1, 21):
            val = 1 if request.form.get(f"q{i}") == "on" else 0
            user_input.append(val)

        group1 = sum(user_input[0:6])   
        group2 = sum(user_input[6:14])  
        group3 = sum(user_input[0:20])  
        if group3 == 0:
            prediction = -2
        elif group1 >= 3 or group2 >= 4:
            prediction = 2  # Urgent
        elif group1 >= 2 or group2 >= 2 or group1+group2 >=2:
            prediction = 1  # YES
        elif model:              # model
            prediction = model.predict(np.array(user_input).reshape(1, -1))[0]
        else:
            prediction = -1  # error flag

        # Result

        if prediction == -2:
            result = "Please Select Atleast One Checkbox"
            pred_val = "n/a"
        elif prediction == 2:
            result = "You Urgently Need The Remedy"
            pred_val = "Urgently Needed"
        elif prediction == 1:
            result = "You Need The Remedy"
            pred_val = "Needed"
        elif prediction == 0:
            result = "Take Potential Preventive Actions"
            pred_val = "Preventive"
        else:
            result = "Sorry, Something Went Wrong!"
            pred_val = "N/A"

        # Save to Google Sheett

        row_data = [datetime.now().strftime("%d-%m-%Y"),name, email] + ["Yes" if x == 1 else "No" for x in user_input] + [pred_val]
        sheet.append_row(row_data)

        return redirect(url_for("response_page", status=result))

    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/response')
def response_page():
    status = request.args.get("status", "No Status Provided")
    return render_template("response.html", status=status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
