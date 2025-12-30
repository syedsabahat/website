from flask import Flask, render_template, abort
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLES_DIR = os.path.join(BASE_DIR, "articles")


@app.route("/")
def home():
    return render_template("user/index.html")

@app.route("/books")
def books():
    books_folder = os.path.join("static", "books")
    books_list = os.listdir(books_folder)
    return render_template("user/books.html", books=books_list)


@app.route("/articles")
def articles():
    files = []

    if os.path.exists(ARTICLES_DIR):
        for f in os.listdir(ARTICLES_DIR):
            if f.endswith(".txt"):
                files.append(f)

    return render_template("user/articles.html", articles=files)


@app.route("/articles/<filename>")
def article_view(filename):
    file_path = os.path.join(ARTICLES_DIR, filename)

    if not os.path.exists(file_path):
        abort(404)

    title = author = date = ""
    content_lines = []
    content_started = False

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()

            if line.startswith("Title:"):
                title = line.replace("Title:", "").strip()
            elif line.startswith("Author:"):
                author = line.replace("Author:", "").strip()
            elif line.startswith("Date:"):
                date = line.replace("Date:", "").strip()
            elif line.startswith("CONTENT:"):
                content_started = True
            elif content_started:
                content_lines.append(line)

    content = "\n".join(content_lines)

    return render_template(
        "user/article_view.html",
        title=title,
        author=author,
        date=date,
        content=content
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

