from flask import Flask, render_template, request
import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

NPOINT_URL = os.getenv("NPOINT_URL")
MY_EMAIL = os.getenv("MY_EMAIL")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_SERVER = os.getenv("SMTP_SERVER")

app = Flask(__name__)

posts = requests.get(NPOINT_URL).json()

@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        message = request.form["message"]
        email = request.form["email"]
        print()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr= EMAIL,
                to_addrs= MY_EMAIL,
                msg= (f"Subject: New Message!\n\n"
                    f"Name: {name}\n Phone: {phone}\n Message: {message}\n Email: {email}"
                      ).encode("utf-8")
            )
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
