from flask import Flask, request, jsonify, render_template, redirect, url_for
import pymysql

app = Flask(__name__)

# Database connection
def db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="12345",
        db="student_management_system",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    return render_template('index.html')

# Route to get all students
@app.route('/students', methods=['GET'])
def get_students():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student_table")
    students = cursor.fetchall()
    conn.close()
    return jsonify(students)

# Route to add a new student
@app.route('/students', methods=['POST'])
def add_student():
    new_student = request.json
    conn = db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO Student_table (FirstName, LastName, DOB, Gender, Email, PhoneNumber, Address, StudentTypeID)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (new_student['FirstName'], new_student['LastName'], new_student['DOB'], new_student['Gender'],
                         new_student['Email'], new_student['PhoneNumber'], new_student['Address'], new_student['StudentTypeID']))
    conn.commit()
    conn.close()
    return "Student added successfully!", 201

# Route to get a student by ID
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student_table WHERE StudentID = %s", (id,))
    student = cursor.fetchone()
    conn.close()
    return jsonify(student)

# Route to update a student
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    updated_student = request.json
    conn = db_connection()
    cursor = conn.cursor()
    sql = """UPDATE Student_table SET FirstName=%s, LastName=%s, DOB=%s, Gender=%s, Email=%s, PhoneNumber=%s, Address=%s, StudentTypeID=%s
             WHERE StudentID=%s"""
    cursor.execute(sql, (updated_student['FirstName'], updated_student['LastName'], updated_student['DOB'], updated_student['Gender'],
                         updated_student['Email'], updated_student['PhoneNumber'], updated_student['Address'], updated_student['StudentTypeID'], id))
    conn.commit()
    conn.close()
    return "Student updated successfully!", 200

# Route to delete a student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Student_table WHERE StudentID = %s", (id,))
    conn.commit()
    conn.close()
    return "Student deleted successfully!", 200

if __name__ == '__main__':
    app.run(debug=True)
