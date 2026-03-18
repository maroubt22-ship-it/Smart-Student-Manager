# Docker Quick Reference - Smart Student Manager

## ⚡ TL;DR - Just the Commands

### Option 1: Docker Compose (Easiest)
```bash
cd "C:\Users\pc\Desktop\Smart Student Manager"
docker-compose up
# Open: http://localhost:5000
```

### Option 2: Docker CLI (Manual)
```bash
# Build the image
docker build -t smart-student-manager:latest .

# Run the container
docker run -d -p 5000:5000 --name student-manager smart-student-manager:latest

# Check status
docker ps

# Open: http://localhost:5000

# View logs
docker logs -f student-manager

# Stop the container
docker stop student-manager
```

---

## 🎯 Essential Commands Cheat Sheet

| Command | What It Does |
|---------|-------------|
| `docker build -t smart-student-manager:latest .` | Build Docker image |
| `docker run -d -p 5000:5000 --name student-manager smart-student-manager:latest` | Run container |
| `docker ps` | List running containers |
| `docker logs -f student-manager` | View live logs |
| `docker stop student-manager` | Stop container |
| `docker start student-manager` | Start container again |
| `docker rm student-manager` | Delete container |
| `docker rmi smart-student-manager:latest` | Delete image |
| `docker-compose up` | Start with Docker Compose |
| `docker-compose down` | Stop Docker Compose |

---

## 📦 What Changed in Your Project

### app.py
- Changed `host='localhost'` → `host='0.0.0.0'`
- Flask now listens to all network interfaces (required for Docker)

### Dockerfile
- Multi-stage build for optimization
- Python 3.11-slim base image
- Virtual environment for dependencies
- Non-root user for security
- Health check included

### requirements.txt
- Added all Flask dependencies explicitly
- Better version pinning

### New Files Added
- `Dockerfile` - Container configuration
- `.dockerignore` - Exclude files from build
- `docker-compose.yml` - Simplified container management
- `DOCKER_GUIDE.md` - Detailed documentation
- `DOCKER_QUICK_REFERENCE.md` - This file

---

## ✅ Verification Checklist

After running the container:

- [ ] Container is running: `docker ps`
- [ ] App is accessible: http://localhost:5000
- [ ] Can add students: Fill form and submit
- [ ] Can view students: Check students page
- [ ] Can delete students: Click delete button
- [ ] Database persists: Data survives container restart

---

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| Port 5000 in use | Use different port: `-p 5001:5000` |
| "Cannot find module" | `docker build --no-cache ...` |
| Container exits immediately | `docker logs student-manager` |
| Permission denied | Restart Docker daemon or restart PC |
| Can't access http://localhost:5000 | Make sure container is running: `docker ps` |

---

**Everything is configured and ready to go!** 🚀
