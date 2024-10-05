from flask import Flask, request, jsonify
import mysql.connector
import random

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mood_book_db"
)

@app.route('/recommend', methods=['POST'])
def recommend_book():
    print("Received POST request on /recommend")  # Log when the route is hit
    # Get the mood from the request
    user_mood = request.json.get('mood')
    print(f"Mood received: {user_mood}")  # Log the mood received

    if not user_mood:
        print("No mood provided, returning 400")
        return jsonify({"error": "Mood is required"}), 400

    cursor = db.cursor(dictionary=True)

    # Query the database for books matching the user's mood
    query = "SELECT book_name FROM books WHERE mood = %s"
    cursor.execute(query, (user_mood,))
    
    # Fetch all books for the mood
    books = cursor.fetchall()
    print(f"Books fetched: {books}")  # Log the books fetched

    if not books:
        print("No books found for this mood, returning 404")
        return jsonify({"error": "No books found for this mood"}), 404

    # Select a random book
    recommended_book = random.choice(books)
    print(f"Recommended book: {recommended_book['book_name']}")  # Log the book recommended

    return jsonify({"book": recommended_book['book_name']})

if __name__ == '__main__':
    print("Starting Flask server...")  # Log when Flask server starts
    app.run(host='localhost', port=5000, debug=True)
