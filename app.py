from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
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

            # ✅ Handle multiple uploaded documents (optional)
            documents = request.files.getlist("document")
            document_paths = []

            for doc in documents:
                if not doc:  # no file object
                    continue
                if not doc.filename or doc.filename.strip() == "":  # empty name
                    continue

                os.makedirs("uploads", exist_ok=True)
                path = os.path.join("uploads", doc.filename)
                doc.save(path)
                document_paths.append(path)

            # ✅ Handle Excel file (mandatory)
            excel_file = request.files["excel"]
            excel_path = "emails.xlsx"
            excel_file.save(excel_path)

            df = pd.read_excel(excel_path)

            # ✅ Setup SMTP server
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

                # ✅ Attach all uploaded documents (if any)
                for path in document_paths:
                    if os.path.exists(path):
                        with open(path, "rb") as f:
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                "Content-Disposition",
                                f"attachment; filename={os.path.basename(path)}"
                            )
                            msg.attach(part)

                server.sendmail(your_email, recipient, msg.as_string())

            server.quit()

            # ✅ Remove temporary files
            for path in document_paths:
                if os.path.exists(path):
                    os.remove(path)
            if os.path.exists(excel_path):
                os.remove(excel_path)

            flash("✅ Emails sent successfully!", "success")

        except Exception as e:
            flash(f"❌ Error: {str(e)}", "error")

        return redirect(url_for("index"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
