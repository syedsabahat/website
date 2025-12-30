from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "super_secret_admin_key"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            session["admin"] = True
            return redirect("/upload")
        return "Invalid credentials"

    return render_template("admin/login_admin.html")


@app.route("/add-article", methods=["GET", "POST"])
def add_article():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        content = request.form["content"]

        os.makedirs("articles", exist_ok=True)

        filename = title.replace(" ", "_") + ".txt"
        path = os.path.join("articles", filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Title: {title}\n")
            f.write(f"Author: {author}\n\n")
            f.write("CONTENT:\n")
            f.write(content)

        return "Article Published Successfully"

    return render_template("admin/add_article.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if not session.get("admin"):
        return redirect("/")

    if request.method == "POST":
        file = request.files["pdf"]
        if file and file.filename.endswith(".pdf"):
            os.makedirs("static/books", exist_ok=True)
            file.save(os.path.join("static/books", file.filename))
            return "Upload successful"

    return render_template("admin/upload.html")

if __name__ == "__main__":
    app.run(debug=True, port=5005)
