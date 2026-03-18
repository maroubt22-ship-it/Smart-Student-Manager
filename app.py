"""
Smart Student Manager - Flask Web Application with MySQL
A modern web application for managing student information
using Flask, SQLAlchemy ORM, and MySQL database.

Database Connection:
- Host: mysqlTaoufiq (Docker container name)
- Username: root
- Password: root123
- Database: smart_student_db
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os

# ============================================
# Flask Application Setup
# ============================================
app = Flask(__name__)
app.secret_key = 'smart_student_manager_secret_key'

# ============================================
# MySQL Database Connection Configuration
# ============================================
# Database connection parameters
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root123')
DB_HOST = os.getenv('DB_HOST', 'mysqlTaoufiq')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'smart_student_db')

# SQLAlchemy database URL format: mysql+pymysql://username:password@host:port/database
DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create SQLAlchemy engine (connection pool)
try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,              # Test connection before using
        pool_recycle=3600,               # Recycle connections every hour
        echo=False                       # Set to True for SQL debugging
    )
    
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    print("✓ Database engine created successfully!")
except Exception as e:
    print(f"✗ Database connection error: {e}")
    raise

# SQLAlchemy Base class for model definitions
Base = declarative_base()

# ============================================
# Database Models (ORM)
# ============================================
class Student(Base):
    """
    Student table model.
    Defines the structure and columns for storing student information.
    """
    __tablename__ = "students"
    
    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    field_of_study = Column(String(150), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert model to dictionary for easier manipulation."""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'field_of_study': self.field_of_study,
            'created_at': self.created_at
        }


# ============================================
# Database Initialization
# ============================================
def init_db():
    """
    Create all database tables defined in the models.
    This function is called on application startup to ensure tables exist.
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables initialized successfully!")
    except Exception as e:
        print(f"✗ Database initialization error: {e}")
        raise


def get_db_session() -> Session:
    """
    Create and return a new database session.
    Used for all database queries.
    """
    return SessionLocal()


# ============================================
# Flask Routes
# ============================================

@app.route('/')
def index():
    """
    Home page route - displays welcome page with navigation.
    """
    return render_template('index.html')


@app.route('/students')
def students():
    """
    Students list page - displays all students from MySQL database.
    Fetches data using SQLAlchemy ORM and passes to template.
    """
    try:
        session = get_db_session()
        # Query all students, ordered by creation date (newest first)
        students_data = session.query(Student).order_by(Student.created_at.desc()).all()
        session.close()
        
        return render_template('students.html', students=students_data)
    except Exception as e:
        flash(f'Error loading students: {str(e)}', 'error')
        return render_template('students.html', students=[])


@app.route('/add')
def add_student_page():
    """
    Add student form page - displays the form to add a new student.
    """
    return render_template('add_student.html')


@app.route('/add-student', methods=['POST'])
def add_student():
    """
    Handle student form submission.
    Validates input and inserts student data into MySQL database.
    """
    # Get form data
    name = request.form.get('name', '').strip()
    age_str = request.form.get('age', '').strip()
    field_of_study = request.form.get('field_of_study', '').strip()
    
    # ============================================
    # Input Validation
    # ============================================
    errors = []
    
    # Validate name
    if not name:
        errors.append('Student name is required.')
    elif len(name) < 2:
        errors.append('Student name must be at least 2 characters long.')
    elif len(name) > 100:
        errors.append('Student name must be at most 100 characters long.')
    
    # Validate age
    if not age_str:
        errors.append('Age is required.')
    else:
        try:
            age = int(age_str)
            if age < 5 or age > 100:
                errors.append('Age must be between 5 and 100.')
        except ValueError:
            errors.append('Age must be a valid number.')
    
    # Validate field of study
    if not field_of_study:
        errors.append('Field of study is required.')
    elif len(field_of_study) < 2:
        errors.append('Field of study must be at least 2 characters long.')
    elif len(field_of_study) > 150:
        errors.append('Field of study must be at most 150 characters long.')
    
    # If there are errors, show them
    if errors:
        for error in errors:
            flash(error, 'error')
        return render_template('add_student.html')
    
    # ============================================
    # Insert into Database
    # ============================================
    try:
        session = get_db_session()
        
        # Create new Student object
        new_student = Student(
            name=name,
            age=int(age_str),
            field_of_study=field_of_study
        )
        
        # Add to session and commit
        session.add(new_student)
        session.commit()
        session.close()
        
        flash(f'✓ Student "{name}" added successfully!', 'success')
        return redirect(url_for('students'))
    except Exception as e:
        flash(f'Error adding student: {str(e)}', 'error')
        return render_template('add_student.html')


@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    """
    Delete a student from the MySQL database.
    Takes student_id as parameter and removes from database.
    """
    try:
        session = get_db_session()
        
        # Query student by ID
        student = session.query(Student).filter(Student.id == student_id).first()
        
        if student:
            student_name = student.name
            # Delete student from database
            session.delete(student)
            session.commit()
            flash(f'✓ Student "{student_name}" deleted successfully!', 'success')
        else:
            flash('Student not found.', 'error')
        
        session.close()
    except Exception as e:
        flash(f'Error deleting student: {str(e)}', 'error')
    
    return redirect(url_for('students'))


# ============================================
# Error Handlers
# ============================================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 - Page Not Found errors."""
    return render_template('index.html'), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 - Internal Server Error."""
    flash('An error occurred. Please try again.', 'error')
    return redirect(url_for('index')), 500


# ============================================
# Application Entry Point
# ============================================

if __name__ == '__main__':
    # Initialize database tables on startup
    init_db()
    
    # Run Flask development server
    # debug=True enables auto-reload and better error messages
    # host='0.0.0.0' makes app accessible from all network interfaces (needed for Docker)
    # port=5000 is the default Flask port
    app.run(debug=True, host='0.0.0.0', port=5000)


@app.route('/')
def index():
    """
    Home page route - displays welcome page with navigation.
    """
    return render_template('index.html')


@app.route('/students')
def students():
    """
    Students list page - displays all students in the database.
    Fetches data from SQLite and passes to template.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students ORDER BY created_at DESC')
        students_data = cursor.fetchall()
        conn.close()
        
        return render_template('students.html', students=students_data)
    except Exception as e:
        flash(f'Error loading students: {str(e)}', 'error')
        return render_template('students.html', students=[])


@app.route('/add')
def add_student_page():
    """
    Add student form page - displays the form to add a new student.
    """
    return render_template('add_student.html')


@app.route('/add-student', methods=['POST'])
def add_student():
    """
    Handle student form submission.
    Validates input and inserts student data into database.
    """
    # Get form data
    name = request.form.get('name', '').strip()
    age_str = request.form.get('age', '').strip()
    field_of_study = request.form.get('field_of_study', '').strip()
    
    # Validation
    errors = []
    
    if not name:
        errors.append('Student name is required.')
    elif len(name) < 2:
        errors.append('Student name must be at least 2 characters long.')
    
    if not age_str:
        errors.append('Age is required.')
    else:
        try:
            age = int(age_str)
            if age < 5 or age > 100:
                errors.append('Age must be between 5 and 100.')
        except ValueError:
            errors.append('Age must be a valid number.')
    
    if not field_of_study:
        errors.append('Field of study is required.')
    elif len(field_of_study) < 2:
        errors.append('Field of study must be at least 2 characters long.')
    
    # If there are errors, show them
    if errors:
        for error in errors:
            flash(error, 'error')
        return render_template('add_student.html')
    
    # Insert into database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (name, age, field_of_study)
            VALUES (?, ?, ?)
        ''', (name, int(age_str), field_of_study))
        conn.commit()
        conn.close()
        
        flash(f'✓ Student "{name}" added successfully!', 'success')
        return redirect(url_for('students'))
    except Exception as e:
        flash(f'Error adding student: {str(e)}', 'error')
        return render_template('add_student.html')


@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    """
    Delete a student from the database.
    Takes student_id as parameter and removes from database.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get student name for flash message
        cursor.execute('SELECT name FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        
        if student:
            cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
            conn.commit()
            flash(f'✓ Student "{student["name"]}" deleted successfully!', 'success')
        else:
            flash('Student not found.', 'error')
        
        conn.close()
    except Exception as e:
        flash(f'Error deleting student: {str(e)}', 'error')
    
    return redirect(url_for('students'))


@app.errorhandler(404)
def page_not_found(e):
    """
    Handle 404 - Page Not Found errors.
    """
    return render_template('index.html'), 404


@app.errorhandler(500)
def server_error(e):
    """
    Handle 500 - Internal Server Error.
    """
    flash('An error occurred. Please try again.', 'error')
    return redirect(url_for('index')), 500


if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    
    # Run Flask development server
    # debug=True enables auto-reload and better error messages
    # host='0.0.0.0' makes the app accessible from outside the container
    app.run(debug=True, host='0.0.0.0', port=5000)
