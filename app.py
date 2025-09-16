from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formataddr
from email import encoders
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for flash messages

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            your_email = request.form["email"]
            your_password = request.form["password"]
            from_name = request.form["from_name"]
            subject = request.form["subject"]
            message = request.form["message"]

            document_file = request.files["document"]
            excel_file = request.files["excel"]

            # Save uploaded files temporarily
            document_path = document_file.filename
            excel_path = "emails.xlsx"
            document_file.save(document_path)
            excel_file.save(excel_path)

            df = pd.read_excel(excel_path)

            # Setup SMTP server
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(your_email, your_password)

            for _, row in df.iterrows():
                name = row["Name"]
                recipient = row["Email"]

                msg = MIMEMultipart()
                msg["From"] = from_name
                msg["To"] = recipient
                msg["Subject"] = subject

                # Personalize message
                body = message.replace("{name}", name)
                msg.attach(MIMEText(body, "plain"))

                # Attach resume
                with open(document_path, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={document_path}")
                    msg.attach(part)

                server.sendmail(your_email, recipient, msg.as_string())

            server.quit()

            # Remove temporary files
            os.remove(document_path)
            os.remove(excel_path)

            flash("✅ Emails sent successfully!", "success")
        except Exception as e:
            flash(f"❌ Error: {str(e)}", "error")

        return redirect(url_for("index"))

    return render_template("index.html")
