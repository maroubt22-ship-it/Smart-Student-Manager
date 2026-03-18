# 🚀 QUICK START - MySQL + Flask Docker (Copy & Paste Commands)

## 📋 BEFORE YOU START

**Prerequisites:**
- ✅ Docker Desktop installed
- ✅ MySQL container already running: `mysqlTaoufiq`
- ✅ MySQL credentials: root / root123

**Verify MySQL is running:**
```bash
docker ps | grep mysqlTaoufiq
```

If not running:
```bash
docker start mysqlTaoufiq
```

---

## 🎯 THREE SIMPLE STEPS

### Step 1: Build the Docker Image
```bash
cd "C:\Users\pc\Desktop\Smart Student Manager"
docker build -t smart-student-manager:mysql .
```

**What this does:**
- Reads Dockerfile
- Creates optimized Docker image with Flask + dependencies
- Automatically tags as `smart-student-manager:mysql`

**Expected output:**
```
...
Successfully built abc123def
Successfully tagged smart-student-manager:mysql
```

---

### Step 2: Start with Docker Compose
```bash
docker-compose up
```

**What this does:**
- Starts Flask container
- Connects to MySQL container
- Initializes database tables (auto-creates if missing)
- Flask listens on port 5000

**Expected output:**
```
web_1 | ✓ Database engine created successfully!
web_1 | ✓ Database tables initialized successfully!
web_1 |  * Running on http://0.0.0.0:5000
```

---

### Step 3: Open in Browser
```
http://localhost:5000
```

**That's it!** The app is now running! ✨

---

## 📝 QUICK COMMANDS REFERENCE

### Start/Stop Application
```bash
# Start
docker-compose up

# Start in background
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart
```

### View Logs
```bash
# All logs
docker-compose logs

# Follow logs (live)
docker-compose logs -f

# Flask app only
docker-compose logs -f web
```

### Check Status
```bash
# Running containers
docker ps

# All containers
docker ps -a

# Specific container
docker inspect smart-student-manager
```

### Access MySQL
```bash
# From host (if MySQL is on localhost:3306)
mysql -u root -proot123 -h 127.0.0.1 smart_student_db

# From MySQL container
docker exec -it mysqlTaoufiq mysql -u root -proot123 -D smart_student_db

# Query students
SELECT * FROM students;
```

### Clean Up
```bash
# Stop and remove containers
docker-compose down

# Remove image
docker rmi smart-student-manager:mysql

# Remove everything
docker-compose down -v
```

---

## 🔍 VERIFY EVERYTHING WORKS

```bash
# 1. Check MySQL is running
docker ps | grep mysqlTaoufiq
# Result: Should show "mysqlTaoufiq" in the output

# 2. Check Flask is running
docker ps | grep smart-student-manager
# Result: Should show "smart-student-manager" in the output

# 3. Check logs for errors
docker-compose logs web | grep -i error
# Result: Should show no errors

# 4. Test Flask app
curl http://localhost:5000
# Result: Should return HTML homepage

# 5. Test database
docker exec mysqlTaoufiq mysql -u root -proot123 -D smart_student_db -e "SELECT COUNT(*) FROM students;"
# Result: Should show number of students
```

---

## 🎯 ONE-LINER COMPLETE SETUP

```bash
cd "C:\Users\pc\Desktop\Smart Student Manager" && docker build -t smart-student-manager:mysql . && docker-compose up
```

This single command:
1. Navigates to project
2. Builds image
3. Starts containers
4. All ready at http://localhost:5000

---

## 📊 WHAT'S RUNNING

After `docker-compose up`:

| Component | Status | Port | Access |
|-----------|--------|------|--------|
| Flask App | ✅ Running | 5000 | http://localhost:5000 |
| MySQL | ✅ Running | 3306 | localhost:3306 (already running) |
| Database | ✅ Created | - | smart_student_db |
| Tables | ✅ Created | - | students table |

---

## 🚨 QUICK TROUBLESHOOTING

### Error: "Connection refused"
```bash
# Solution 1: Make sure MySQL is running
docker start mysqlTaoufiq
docker-compose up

# Solution 2: Check docker-compose.yml
# Change DB_HOST=host.docker.internal (for localhost MySQL)
```

### Error: "Port 5000 already in use"
```bash
# Solution: Stop existing container
docker-compose down
docker-compose up
```

### Error: "Can't find module..."
```bash
# Solution: Rebuild image
docker-compose down
docker build --no-cache -t smart-student-manager:mysql .
docker-compose up
```

### Error: "Table doesn't exist"
```bash
# Solution: Restart (auto-creates tables)
docker-compose restart web
```

---

## 💡 DEVELOPMENT WORKFLOW

```bash
# 1. Start app
docker-compose up

# 2. Make code changes
# (Files update automatically due to volume mount)
# Edit app.py or templates

# 3. Test changes
# Refresh http://localhost:5000

# 4. View live logs
docker-compose logs -f

# 5. When done
# Ctrl+C to stop
```

---

## 🎁 USEFUL SHORTCUTS

Save this script as `run.bat` (Windows):
```batch
@echo off
cd "C:\Users\pc\Desktop\Smart Student Manager"
docker-compose up
```

Then just double-click to run!

---

## ✅ FINAL CHECKLIST

Before considering done:
- [ ] `docker-compose up` completes without errors
- [ ] Flask logs show "Running on http://0.0.0.0:5000"
- [ ] http://localhost:5000 loads in browser
- [ ] Homepage displays correctly
- [ ] Can click "Add Student"
- [ ] Form loads
- [ ] Can add a student
- [ ] Student appears in list
- [ ] Can view all students
- [ ] Can delete a student
- [ ] Data persists (refresh page)

---

## 🎯 NEXT STEPS

1. **Now:** Run `docker-compose up`
2. **Test:** Add a student
3. **Explore:** Click around the app
4. **Learn:** Read MYSQL_SETUP_GUIDE.md
5. **Customize:** Modify environment variables as needed

---

## 📞 QUICK HELP

| Need | Command |
|------|---------|
| Start | `docker-compose up` |
| Stop | `Ctrl+C` |
| Logs | `docker-compose logs -f` |
| Status | `docker ps` |
| Rebuild | `docker build --no-cache -t smart-student-manager:mysql .` |
| Clean | `docker-compose down` |
| MySQL | `docker exec -it mysqlTaoufiq mysql -u root -proot123` |
| Error? | `docker-compose logs web` |

---

## 🚀 YOU'RE READY!

```bash
docker-compose up
```

Go to: **http://localhost:5000** ✨

**Everything is set up and ready to use!**
