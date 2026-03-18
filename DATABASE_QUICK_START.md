# 🗄️ Database Setup - Quick Reference

## Current Setup: SQLite (Default)

Your project currently uses **SQLite** - a file-based database that requires zero setup!

```bash
# Just run:
docker-compose up

# App available at: http://localhost:5000
```

---

## 📦 Available Configurations

### 1. SQLite (Current - Development)
```bash
docker-compose up
```
- **File:** `docker-compose.yml`
- **Best for:** Development, testing, learning
- **Database file:** `./database.db`
- **Setup time:** 0 seconds
- **No additional services needed**

### 2. PostgreSQL (Production)
```bash
docker-compose -f docker-compose.postgres.yml up
```
- **File:** `docker-compose.postgres.yml`
- **Best for:** Production, real deployments
- **Database service:** Separate PostgreSQL container
- **Setup time:** 5-10 seconds
- **Includes:** Health checks, automatic initialization

---

## 🔀 What's in Each File

### docker-compose.yml (SQLite)
```yaml
services:
  web:
    # Flask application
    # Database: SQLite (database.db)
    # No additional services
```

### docker-compose.postgres.yml (PostgreSQL)
```yaml
services:
  db:
    # PostgreSQL database server
    image: postgres:15-alpine
    ports: 5432:5432
    
  web:
    # Flask application
    # Database: PostgreSQL (via db service)
    depends_on: [db]
```

---

## 🚀 Database Persistence

Both setups persist data across container restarts:

### SQLite:
```yaml
volumes:
  - ./database.db:/app/database.db  # File on your computer
```

### PostgreSQL:
```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data  # Docker volume
```

---

## 🔧 Commands for Both Setups

```bash
# START
# SQLite:
docker-compose up

# PostgreSQL:
docker-compose -f docker-compose.postgres.yml up

# ───────────────────────────────────

# STOP (Ctrl+C) or run:
# SQLite:
docker-compose down

# PostgreSQL:
docker-compose -f docker-compose.postgres.yml down

# ───────────────────────────────────

# LOGS
# SQLite:
docker-compose logs -f

# PostgreSQL:
docker-compose -f docker-compose.postgres.yml logs -f

# ───────────────────────────────────

# CLEAN UP
# SQLite:
docker-compose down -v

# PostgreSQL:
docker-compose -f docker-compose.postgres.yml down -v
```

---

## 📊 Database Files Provided

| File | Purpose | Status |
|------|---------|--------|
| `docker-compose.yml` | SQLite development setup | ✅ Ready |
| `docker-compose.postgres.yml` | PostgreSQL production setup | ✅ Ready |
| `DATABASE_SETUP_GUIDE.md` | Complete migration guide | ✅ Detailed |
| `requirements-with-postgres.txt` | Packages for PostgreSQL | ✅ Included |
| `Dockerfile` | Container image | ✅ Compatible with both |
| `app.py` | Flask application | ⚠️ Works with SQLite only (needs modification for PostgreSQL) |

---

## ✅ Recommendations

- **Just starting?** → Use SQLite (default)
  ```bash
  docker-compose up
  ```

- **Testing locally?** → Use SQLite (no overhead)
  ```bash
  docker-compose up
  ```

- **Ready for production?** → Use PostgreSQL
  ```bash
  docker-compose -f docker-compose.postgres.yml up
  ```

- **Team development?** → Use PostgreSQL (shared database)
  ```bash
  docker-compose -f docker-compose.postgres.yml up
  ```

---

## 🔄 How to Switch Between Databases

### Current Status: SQLite ✓

### To Switch to PostgreSQL:

1. **Backup your SQLite data:**
   ```bash
   cp database.db database.db.backup
   ```

2. **Update app.py** (see DATABASE_SETUP_GUIDE.md)

3. **Use PostgreSQL compose file:**
   ```bash
   docker-compose -f docker-compose.postgres.yml up
   ```

4. **Your data will be in PostgreSQL** (not SQLite)

---

## 🎁 Bonus: Quick Switching

Create aliases for easier switching:

### Windows (PowerShell):
```powershell
# Add to your PowerShell profile
Set-Alias -Name dev 'docker-compose up'
Set-Alias -Name prod 'docker-compose -f docker-compose.postgres.yml up'

# Usage:
dev    # Start SQLite
prod   # Start PostgreSQL
```

### Mac/Linux (Bash):
```bash
# Add to ~/.bashrc or ~/.zshrc
alias dev='docker-compose up'
alias prod='docker-compose -f docker-compose.postgres.yml up'

# Usage:
dev    # Start SQLite
prod   # Start PostgreSQL
```

---

## 📈 Database Size Limits

| Database | Small DB | Large DB |
|----------|----------|----------|
| SQLite | ✅ <100MB | ⚠️ Slow |
| PostgreSQL | ✅ <100MB | ✅ Fast |

---

## 🔒 Security Notes

### SQLite:
- File-based, no password needed
- Suitable for development only
- Not secure for production

### PostgreSQL:
- Username/password authentication
- Change defaults in production!
- Suitable for production

**Default PostgreSQL Credentials:**
```
User: student_user
Pass: secure_password_123
DB:   smart_student_db
```

**Change these in production!**

---

## 🆘 Troubleshooting

### "Port 5000 already in use"
```bash
docker-compose down
# or use different port:
docker-compose up -p 5001:5000
```

### "Cannot connect to database"
```bash
# Restart the service
docker-compose restart
```

### "Database is empty"
```bash
# Container reinitializes database on first run
docker-compose up
```

### "Want to see database contents"
```bash
# SQLite:
sqlite3 database.db
SELECT * FROM students;

# PostgreSQL:
docker exec -it smart-student-manager-db psql -U student_user -d smart_student_db
SELECT * FROM students;
```

---

## 📞 Support

- **SQLite Questions?** → See README.md
- **Docker Questions?** → See DOCKER_GUIDE.md
- **Database Setup?** → See DATABASE_SETUP_GUIDE.md
- **Quick commands?** → This file!

---

**Status: ✅ Ready to Deploy**

Choose your database and start! 🚀
