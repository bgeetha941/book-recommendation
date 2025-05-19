
from flask import Flask, render_template, request, url_for
import pandas as pd
import os

app = Flask(__name__)

def get_genre(title):
    title = title.lower()
    if 'harry potter' in title: return 'Fantasy'
    elif 'hitchhiker' in title: return 'Sci-Fi'
    elif 'history' in title or 'collapse' in title: return 'History'
    elif 'diary' in title or 'travel' in title: return 'Travel'
    elif 'music' in title: return 'Music'
    elif 'tesla' in title or 'inventions' in title or 'wizard' in title: return 'Biography'
    elif 'programming' in title or 'html' in title or 'css' in title or 'ruby' in title: return 'Programming'
    elif 'zen' in title or 'philosophy' in title: return 'Philosophy'
    elif 'war' in title or 'peace' in title: return 'War'
    elif 'motorcycle' in title: return 'Adventure'
    elif 'logo' in title: return 'Design'
    else: return 'General'

def get_fallback_images():
    genres = ['Fantasy', 'History', 'Sci-Fi', 'Travel', 'Music', 'Biography', 'Programming', 'Philosophy', 'War', 'Adventure', 'Design', 'General']
    return {genre: url_for('static', filename=f'default_{genre.lower()}.jpg') for genre in genres}

def extract_books():
    df = pd.read_csv("books.csv", on_bad_lines='skip')
    fallback_images = get_fallback_images()
    books = []

    for _, row in df.iterrows():
        title = str(row.get("title", "Untitled"))
        isbn = str(row.get("isbn", "")).strip()
        genre = get_genre(title)
        cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg" if isbn else ""
        preview_path = os.path.join("static/books", isbn, "content.txt")
        preview = ""
        if os.path.exists(preview_path):
            with open(preview_path, "r", encoding='utf-8') as f:
                preview = f.read()

        books.append({
            "bookID": row.get("bookID", ""),
            "title": title,
            "authors": row.get("authors", "Unknown"),
            "average_rating": row.get("average_rating", "N/A"),
            "genre": genre,
            "image": cover_url,
            "fallback": fallback_images.get(genre, fallback_images["General"]),
            "isbn": isbn,
            "isbn13": row.get("isbn13", ""),
            "language_code": row.get("language_code", ""),
            "ratings_count": row.get("ratings_count", 0),
            "text_reviews_count": row.get("text_reviews_count", 0),
            "publication_date": row.get("publication_date", "N/A"),
            "publisher": row.get("publisher", "Unknown"),
            "preview": preview
        })
    return books

@app.route("/")
def index():
    selected_genre = request.args.get("genre")
    books = extract_books()
    if selected_genre:
        books = [book for book in books if book["genre"] == selected_genre]
    genres = sorted(set(book["genre"] for book in books))
    return render_template("index.html", books=books, genres=genres)

@app.route("/book/<isbn>")
def book_detail(isbn):
    books = extract_books()
    book = next((b for b in books if b['isbn'] == isbn), None)
    if book:
        return render_template("book_detail.html", book=book)
    return "Book not found", 404

if __name__ == "__main__":
    app.run(debug=True)

