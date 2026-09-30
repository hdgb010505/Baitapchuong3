from flask import Flask, render_template, request, jsonify, url_for
from markupsafe import escape

app = Flask(__name__)

# 1. Khởi tạo danh sách BOOKS (≥ 4 cuốn)
BOOKS = [
    {
        "id": 1,
        "title": "Lập trình Python cơ bản",
        "author": "Nguyễn Văn A",
        "year": 2021,
        "category": "Lập trình",
        "available": True
    },
    {
        "id": 2,
        "title": "Flask Web Development",
        "author": "Miguel Grinberg",
        "year": 2018,
        "category": "Lập trình",
        "available": True
    },
    {
        "id": 3,
        "title": "Cơ sở dữ liệu",
        "author": "Trần Thị B",
        "year": 2020,
        "category": "Cơ sở dữ liệu",
        "available": False
    },
    {
        "id": 4,
        "title": "Học máy cho người mới bắt đầu",
        "author": "Lê Văn C",
        "year": 2022,
        "category": "Trí tuệ nhân tạo",
        "available": True
    }
]

# 2. Trang chủ /
@app.route("/")
def index():
    total_books = len(BOOKS)
    available_books = sum(1 for b in BOOKS if b["available"])
    return render_template("index.html", total_books=total_books, available_books=available_books)

# 3. Trang /books
@app.route("/books")
def book_list():
    selected_category = request.args.get("category", "").strip()
    categories = list(set(b["category"] for b in BOOKS))
    
    if selected_category:
        filtered_books = [b for b in BOOKS if b["category"] == selected_category]
    else:
        filtered_books = BOOKS
        
    return render_template(
        "books.html", 
        books=filtered_books, 
        categories=categories, 
        selected_category=selected_category
    )

# 4. Trang /books/<int:book_id>
@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        safe_id = escape(book_id)
        return render_template("404.html", message=f"Không có sách với ID = {safe_id}"), 404
    
    return render_template("detail.html", book=book)

# 5. API routes
@app.route("/api/books")
def api_books():
    return jsonify(BOOKS)

@app.route("/api/books/<int:book_id>")
def api_book_detail(book_id):
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": f"Không có sách với ID = {book_id}"}), 404
    return jsonify(book)

# 6. Trang 404
@app.errorhandler(404)
def page_not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Resource not found"}), 404
    return render_template("404.html", message="Trang bạn tìm kiếm không tồn tại."), 404

# Quan trọng: Đoạn này để giữ ứng dụng luôn chạy
if __name__ == "__main__":
    app.run(debug=True)