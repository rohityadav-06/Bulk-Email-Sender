
# 📧 Bulk Email Automation with Flask & Python

This project allows you to send **personalized bulk emails** with attachments (like resumes, invitations, etc.) using Python and Flask.  
It reads recipient data from an Excel file and sends emails via Gmail SMTP (or SendGrid for deployment).

---

## 🚀 Features
- Upload Excel file with `Name` and `Email` columns.
- Send personalized emails (`Hi {name}, ...`).
- Attach any document (PDF, DOCX, etc.).
- Flask web interface with modern UI.
- Secure credentials handling with environment variables.

---

## 📂 Project Structure
```
email_automation_app/
│── app.py              # Flask backend
│── requirements.txt    # Dependencies
│── Procfile            # For deployment (Render/Heroku)
│── templates/
│    └── index.html     # Frontend form (UI)
│── static/
     └── style.css      # Styling
```

---

## ⚙️ Installation (Local)
1. Clone this repo:
   ```bash
   git clone https://github.com/your-username/email-automation-app.git
   cd email-automation-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run Flask app:
   ```bash
   python app.py
   ```

4. Open in browser:
   ```
   http://127.0.0.1:5000/
   ```

---

## 📊 Excel Format
Your Excel file must have these columns:

| Name       | Email                |
|------------|----------------------|
| John Doe   | john@example.com     |
| Jane Smith | jane.smith@test.com  |

---

## 🔑 Gmail Setup
1. Enable **2-Step Verification** in your Google Account.  
2. Create an **App Password** (not your normal Gmail password).  
3. Use that App Password in the app.  

⚠️ If you deploy on Render/Heroku, Gmail may block SMTP. In that case, use **SendGrid**.

---

## ☁️ Deployment
### Render (Free Hosting)
1. Push your code to GitHub.
2. Add `requirements.txt` and `Procfile`.
3. Connect GitHub repo to [Render](https://render.com).
4. Set **Environment Variables** in Render Dashboard:
   ```
   EMAIL_USER=youremail@gmail.com
   EMAIL_PASS=yourapppassword
   SECRET_KEY=anyrandomstring
   ```
5. Deploy 🎉

### SendGrid (Recommended for Production)
- Free 100 emails/day.  
- Replace Gmail SMTP code with SendGrid API for better reliability.

---

## 🛠️ Requirements
- Python 3.9+
- Flask
- pandas
- openpyxl
- gunicorn (for deployment)

Install with:
```bash
pip install flask pandas openpyxl gunicorn
```

---

## ✨ Future Improvements
- Add support for multiple attachments.
- Use SendGrid by default for deployment.
- Add a database for email history tracking.

---

## 👨‍💻 Author
Built by **Rohit Yadav** 🚀  
Feel free to fork & improve this project!
