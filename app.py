from flask import Flask, request, jsonify, render_template
import pymysql

app = Flask(__name__)

# Database connection
def db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        db="student_management_system",
        cursorclass=pymysql.cursors.DictCursor
    )

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# CRUD operations for Student_table
@app.route('/students', methods=['GET', 'POST'])
def manage_students():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Student_table")
        students = cursor.fetchall()
        return jsonify(students)
    if request.method == 'POST':
        new_student = request.json
        sql = """INSERT INTO Student_table (FirstName, LastName, DOB, Gender, Email, PhoneNumber, Address, StudentTypeID)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (new_student['FirstName'], new_student['LastName'], new_student['DOB'], new_student['Gender'],
                             new_student['Email'], new_student['PhoneNumber'], new_student['Address'], new_student['StudentTypeID']))
        conn.commit()
        return "Student added successfully!", 201

@app.route('/students/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_student(id):
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Student_table WHERE StudentID = %s", (id,))
        student = cursor.fetchone()
        return jsonify(student)
    if request.method == 'PUT':
        updated_student = request.json
        sql = """UPDATE Student_table SET FirstName=%s, LastName=%s, DOB=%s, Gender=%s, Email=%s, PhoneNumber=%s, Address=%s, StudentTypeID=%s
                 WHERE StudentID=%s"""
        cursor.execute(sql, (updated_student['FirstName'], updated_student['LastName'], updated_student['DOB'], updated_student['Gender'],
                             updated_student['Email'], updated_student['PhoneNumber'], updated_student['Address'], updated_student['StudentTypeID'], id))
        conn.commit()
        return "Student updated successfully!", 200
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM Student_table WHERE StudentID = %s", (id,))
        conn.commit()
        return "Student deleted successfully!", 200

# CRUD operations for other tables (Faculty, Lecturer, Unit, StudentType)
@app.route('/<table>', methods=['GET', 'POST'])
def manage_table(table):
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute(f"SELECT * FROM {table}_table")
        records = cursor.fetchall()
        return jsonify(records)
    if request.method == 'POST':
        new_record = request.json
        columns = ', '.join(new_record.keys())
        values = ', '.join(['%s'] * len(new_record))
        sql = f"INSERT INTO {table}_table ({columns}) VALUES ({values})"
        cursor.execute(sql, tuple(new_record.values()))
        conn.commit()
        return f"{table} record added successfully!", 201

@app.route('/<table>/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_table_record(table, id):
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute(f"SELECT * FROM {table}_table WHERE {table}ID = %s", (id,))
        record = cursor.fetchone()
        return jsonify(record)
    if request.method == 'PUT':
        updated_record = request.json
        updates = ', '.join([f"{k}=%s" for k in updated_record.keys()])
        sql = f"UPDATE {table}_table SET {updates} WHERE {table}ID = %s"
        cursor.execute(sql, tuple(updated_record.values()) + (id,))
        conn.commit()
        return f"{table} record updated successfully!", 200
    if request.method == 'DELETE':
        cursor.execute(f"DELETE FROM {table}_table WHERE {table}ID = %s", (id,))
        conn.commit()
        return f"{table} record deleted successfully!", 200

if __name__ == '__main__':
    app.run(debug=True)
