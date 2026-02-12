from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)   # allow frontend access

def init_db():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            role TEXT,
            department TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/employees', methods=['GET', 'POST'])
def employees():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.json
        cursor.execute(
            "INSERT INTO employees (name, email, role, department) VALUES (?, ?, ?, ?)",
            (data['name'], data['email'], data['role'], data['department'])
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Employee added successfully"}), 201

    cursor.execute("SELECT name, email, role, department FROM employees")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
