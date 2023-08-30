from flask import Flask, jsonify, request
import pandas as pd, csv

BOOK_FILE = "books.csv"

app = Flask(__name__)

@app.route("/")
def home():
    return "home"

@app.route("/health")
def health():
    return "Alive and kicking!"


@app.route("/books", methods=['GET'])
def book_list():
    books = []
    books_table = pd.read_csv(BOOK_FILE)

    for i in range(0, len(books_table)):
        books.append({
            'id': int(books_table["id"][i]),
            'title': books_table["title"][i],
            'rating': books_table["rating"][i],
            'price': books_table["price"][i]
        })
    return books

@app.route("/books", methods=['POST'])
def add():
    my_request = request.get_json()
    csv_writer(my_request)
    return my_request

@app.route('/books/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        df = pd.read_csv(BOOK_FILE)
        df = df.drop(df[df["id"] == id].index)
        df.to_csv(BOOK_FILE, index=False)
    except:
        return f'ERROR: ID: {id} not deleted'
    return f'ID: {id} deleted'

def csv_writer(content):
    field_names = ("id","title","rating","price","language")
    with open(BOOK_FILE, 'a', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writerow(content)

app.run(port=5000, host='localhost', debug=True)