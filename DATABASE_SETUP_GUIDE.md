# Database Configuration Guide - Smart Student Manager

## 📊 Database Options

You have two database options:

| Feature | SQLite | PostgreSQL |
|---------|--------|-----------|
| **Type** | File-based | Server-based |
| **Best For** | Development, Small deployments | Production, Multi-user |
| **Setup** | No setup needed | Requires separate service |
| **Scalability** | Limited | Excellent |
| **Concurrent Users** | 1-5 | 100+ |
| **Data Size** | Small (~1GB) | Large (unlimited) |
| **Backup** | Simple file copy | More complex |
| **Docker Compose** | Simple | Requires postgres service |

---

## ✅ Current Setup: SQLite (Development)

Your current configuration uses **SQLite**, which is perfect for:
- Local development
- Testing
- Small deployments
- Learning Flask

### Run SQLite Version:
```bash
docker-compose up
```

### How It Works:
```
Flask Container
    ↓
SQLite Database (database.db in container)
    ↓
Volume Mount (persists on host: ./database.db)
```

---

## 🚀 PostgreSQL: Production-Ready Setup

For production deployments, use PostgreSQL.

### Run PostgreSQL Version:
```bash
docker-compose -f docker-compose.postgres.yml up
```

### What This Does:
```
Flask Container (Port 5000)
    ↓
PostgreSQL Container (Port 5432)
    ↓
Persistent Data Volume
```

### Features:
- ✅ Separate database service
- ✅ Automatic health checks
- ✅ Data persistence
- ✅ Connection pooling ready
- ✅ Backup-friendly
- ✅ Multi-user support

---

## 🔄 How to Switch from SQLite to PostgreSQL

### Step 1: Update requirements.txt

Add PostgreSQL driver:
```bash
# Option A: Add to existing requirements.txt
pip install psycopg2-binary
```

Or add this line to `requirements.txt`:
```
psycopg2-binary==2.9.9
SQLAlchemy==2.0.23
```

### Step 2: Modify app.py

Replace the SQLite database code with PostgreSQL:

**Original (SQLite):**
```python
import sqlite3
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
```

**Updated (PostgreSQL):**
```python
import psycopg2
from psycopg2.extras import RealDictCursor
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://student_user:secure_password_123@localhost:5432/smart_student_db')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn
```

### Step 3: Update Database Initialization

**Original (SQLite):**
```python
def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (...)
        ''')
        conn.commit()
        conn.close()
```

**Updated (PostgreSQL):**
```python
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INTEGER NOT NULL,
                field_of_study VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("✓ Database initialized successfully!")
    except Exception as e:
        print(f"Database already exists or error: {e}")
```

### Step 4: Use PostgreSQL Compose File

```bash
docker-compose -f docker-compose.postgres.yml up
```

Or rename it:
```bash
mv docker-compose.yml docker-compose.sqlite.yml
mv docker-compose.postgres.yml docker-compose.yml
docker-compose up
```

---

## 📁 File Structure After Database Setup

```
Smart Student Manager/
├── app.py                              (Updated for PostgreSQL)
├── requirements.txt                    (Added psycopg2)
├── Dockerfile
├── docker-compose.yml                  (Original - SQLite)
├── docker-compose.sqlite.yml           (SQLite version)
├── docker-compose.postgres.yml         (PostgreSQL version)
├── DATABASE_SETUP_GUIDE.md             (This file)
├── database.db                         (SQLite - auto-created)
├── templates/
├── static/
└── .dockerignore
```

---

## 🔑 PostgreSQL Credentials (Change in Production!)

**Default Credentials:**
```
Username: student_user
Password: secure_password_123
Database: smart_student_db
Host: db (internal)
Port: 5432
```

**Change in Production:**
```yaml
# In docker-compose.postgres.yml
environment:
  - POSTGRES_USER=your_username
  - POSTGRES_PASSWORD=your_strong_password_12345
  - POSTGRES_DB=your_database_name
```

And update environment in Flask service:
```yaml
environment:
  - DATABASE_URL=postgresql://your_username:your_strong_password_12345@db:5432/your_database_name
```

---

## 💾 Data Persistence

### SQLite:
```yaml
volumes:
  - ./database.db:/app/database.db
```
Database file is stored on your host machine.

### PostgreSQL:
```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```
Data is stored in Docker volume (preserved across container restarts).

---

## 🔄 Database Queries Differences

### Query Style Change

**SQLite:**
```python
cursor.execute('SELECT * FROM students WHERE age > ?', (age,))
```

**PostgreSQL:**
```python
cursor.execute('SELECT * FROM students WHERE age > %s', (age,))
cursor.execute('SELECT * FROM students WHERE age > %(age)s', {'age': age})
```

**Key Difference:**
- SQLite uses `?` for parameters
- PostgreSQL uses `%s` for parameters

### Example Update for app.py:

**Before (SQLite):**
```python
cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
cursor.execute('INSERT INTO students (name, age, field_of_study) VALUES (?, ?, ?)', 
               (name, int(age_str), field_of_study))
```

**After (PostgreSQL):**
```python
cursor.execute('SELECT * FROM students WHERE id = %s', (student_id,))
cursor.execute('DELETE FROM students WHERE id = %s', (student_id,))
cursor.execute('INSERT INTO students (name, age, field_of_study) VALUES (%s, %s, %s)', 
               (name, int(age_str), field_of_study))
```

---

## 🔧 Common Commands

### SQLite Version:
```bash
# Start
docker-compose up

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Access database (from host)
sqlite3 database.db
```

### PostgreSQL Version:
```bash
# Start
docker-compose -f docker-compose.postgres.yml up

# Stop
docker-compose -f docker-compose.postgres.yml down

# View logs
docker-compose -f docker-compose.postgres.yml logs -f

# Connect to database
docker exec -it smart-student-manager-db psql -U student_user -d smart_student_db

# SQL Commands in psql:
# \dt                    - List tables
# \d students            - Show students table structure
# SELECT * FROM students; - Query students
# \q                     - Quit
```

---

## 🧪 Testing Connection

### Test SQLite:
```bash
docker exec smart-student-manager python -c "
import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM students')
print(f'Total students: {cursor.fetchone()[0]}')
"
```

### Test PostgreSQL:
```bash
docker exec smart-student-manager python -c "
import psycopg2
conn = psycopg2.connect('postgresql://student_user:secure_password_123@db:5432/smart_student_db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM students')
print(f'Total students: {cursor.fetchone()[0]}')
"
```

---

## 📊 Performance Comparison

| Operation | SQLite | PostgreSQL |
|-----------|--------|-----------|
| Add student | ~5ms | ~10ms |
| List students | ~50ms | ~100ms |
| Delete student | ~5ms | ~8ms |
| Concurrent writes | ❌ Locks | ✅ Handles well |
| Max students | 100K | 1M+ |

**Note:** PostgreSQL is slightly slower for single operations but handles concurrency much better.

---

## 🚀 Deployment Scenarios

### Scenario 1: Local Development
```bash
# Use SQLite (no setup needed)
docker-compose up
```

### Scenario 2: Team Development
```bash
# Use PostgreSQL (shared database)
docker-compose -f docker-compose.postgres.yml up
```

### Scenario 3: Production Deployment
```bash
# Use PostgreSQL with external database service
# Configure database.env file with production credentials
docker-compose -f docker-compose.postgres.yml up -d
```

---

## 🔒 Security Tips

### Don't Do This (Hardcoding):
```python
DATABASE_URL = 'postgresql://user:password@host:5432/db'
```

### Do This (Environment Variables):
```python
import os
DATABASE_URL = os.getenv('DATABASE_URL')
```

### Use .env File:
```bash
# Create .env file
DATABASE_URL=postgresql://user:password@db:5432/db
SECRET_KEY=your_secret_key_12345
FLASK_ENV=production
```

```python
# app.py
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
```

---

## 🔄 Backup Strategies

### SQLite Backup:
```bash
# Copy database file
cp database.db database.db.backup

# Or use Docker
docker cp smart-student-manager:/app/database.db ./backup.db
```

### PostgreSQL Backup:
```bash
# Full backup
docker exec smart-student-manager-db pg_dump -U student_user smart_student_db > backup.sql

# Restore from backup
docker exec -i smart-student-manager-db psql -U student_user smart_student_db < backup.sql
```

---

## 📈 Scaling Considerations

### SQLite Limitations:
- Single file bottleneck
- No horizontal scaling
- Read-heavy optimization needed
- Max ~100 concurrent connections

### PostgreSQL Advantages:
- Multi-machine replication
- Master-slave setup
- Read replicas for scaling
- Connection pooling

---

## 🐛 Troubleshooting

### PostgreSQL Connection Refused:
```bash
# Check if database container is running
docker ps

# View logs
docker-compose -f docker-compose.postgres.yml logs db

# Restart database
docker-compose -f docker-compose.postgres.yml restart db
```

### "relation does not exist" Error:
```bash
# Database not initialized, run init_db function
docker-compose -f docker-compose.postgres.yml restart web
```

### "too many connections" Error:
```yaml
# Increase in docker-compose.postgres.yml
environment:
  - POSTGRES_INITDB_ARGS=-c max_connections=500
```

---

## 📚 Additional Resources

- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **psycopg2 Docs**: https://www.psycopg.org/
- **Docker Postgres Image**: https://hub.docker.com/_/postgres

---

**Summary:**
- **Starting out?** Use SQLite version (default)
- **Scaling up?** Switch to PostgreSQL version
- **Production?** Use PostgreSQL with volumes and backups

All files are in place. Choose your setup and deploy! 🚀
