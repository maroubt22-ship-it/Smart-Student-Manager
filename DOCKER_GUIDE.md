# Smart Student Manager - Docker Deployment Guide

## 📦 Overview

This guide explains how to Dockerize and run the Smart Student Manager Flask application using Docker.

Docker packages your application with all dependencies into a containerized environment that runs consistently everywhere - on your laptop, servers, or cloud platforms.

---

## 🚀 Quick Start (Easiest Method)

### Using Docker Compose (Recommended for Beginners)

```bash
cd "C:\Users\pc\Desktop\Smart Student Manager"
docker-compose up
```

That's it! Your app will be running at `http://localhost:5000`

---

## 🐳 Docker Build & Run (Manual Method)

### Step 1: Build the Docker Image

```bash
# Navigate to project directory
cd "C:\Users\pc\Desktop\Smart Student Manager"

# Build the image with a tag
docker build -t smart-student-manager:latest .
```

**What this command does:**
- `docker build` - Creates a Docker image from the Dockerfile
- `-t smart-student-manager:latest` - Tags the image with a name and version
- `.` - Uses the Dockerfile in the current directory

**Expected output:**
```
Successfully built abc123def456
Successfully tagged smart-student-manager:latest
```

### Step 2: Run the Container

```bash
# Run the container with port mapping
docker run -d -p 5000:5000 --name student-manager smart-student-manager:latest
```

**What this command does:**
- `docker run` - Creates and starts a new container
- `-d` - Runs in detached mode (background)
- `-p 5000:5000` - Maps port 5000 on host to port 5000 in container
- `--name student-manager` - Names the container for easy reference
- `smart-student-manager:latest` - Image to run

**Access the application:**
```
http://localhost:5000
```

---

## 📋 All Docker Commands Reference

### View Running Containers
```bash
docker ps
```

### View All Containers (including stopped)
```bash
docker ps -a
```

### View Images
```bash
docker images
```

### Stop the Container
```bash
docker stop student-manager
```

### Start the Container Again
```bash
docker start student-manager
```

### Remove the Container
```bash
docker rm student-manager
```

### Remove the Image
```bash
docker rmi smart-student-manager:latest
```

### View Container Logs
```bash
docker logs student-manager
```

### Monitor Real-time Logs
```bash
docker logs -f student-manager
```

### Execute Command Inside Container
```bash
docker exec -it student-manager bash
```

---

## 🐳 Docker Compose Commands

### Start Services
```bash
docker-compose up
```

### Start in Background
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs
```

### View Running Services
```bash
docker-compose ps
```

### Rebuild Images
```bash
docker-compose up --build
```

---

## 🔧 Advanced Usage

### Persist Database Across Container Restarts

```bash
# Run with volume for database persistence
docker run -d -p 5000:5000 \
  -v C:\Users\pc\Desktop\Smart Student Manager\database.db:/app/database.db \
  --name student-manager \
  smart-student-manager:latest
```

On Linux/Mac:
```bash
docker run -d -p 5000:5000 \
  -v $(pwd)/database.db:/app/database.db \
  --name student-manager \
  smart-student-manager:latest
```

### Run Interactive Shell (for debugging)

```bash
docker run -it smart-student-manager:latest bash
```

### Set Environment Variables

```bash
docker run -d -p 5000:5000 \
  -e FLASK_ENV=production \
  --name student-manager \
  smart-student-manager:latest
```

---

## 📊 Project Files Explained

### Dockerfile

A multi-stage Docker configuration file with 3 stages:

1. **Base Stage** - Sets up Python environment
2. **Builder Stage** - Creates virtual environment and installs dependencies
3. **Runtime Stage** - Final image with only necessary files

**Key features:**
- `FROM python:3.11-slim` - Base image (lightweight)
- Virtual environment for isolation
- Non-root user for security
- Health check included
- Optimized for caching

### requirements.txt

Lists all Python dependencies:
- Flask - Web framework
- Werkzeug - WSGI utilities
- Flask dependencies (Jinja2, click, etc.)

### .dockerignore

Excludes files from Docker build (like .git, __pycache__, etc.)
- Reduces image size
- Speeds up build

### docker-compose.yml

Simplifies container management:
- Defines service configuration
- Port mapping
- Volume mounting
- Environment variables

---

## 🔍 How It Works

### Container Networking

```
┌─────────────────────────────────────────┐
│         Your Computer (Host)            │
│                                         │
│   Port 5000 ─────────────────────────┐  │
│                                      │  │
│  ┌──────────────────────────────────┘  │
│  │                                     │
│  │  ┌───────────────────────────────┐  │
│  │  │    Docker Container           │  │
│  │  │  ┌─────────────────────────┐  │  │
│  │  │  │  Smart Student Manager  │  │  │
│  │  │  │  Flask on 0.0.0.0:5000  │  │  │
│  │  │  └─────────────────────────┘  │  │
│  │  └───────────────────────────────┘  │
│  │                                     │
│  └─ Port 5000 (container)              │
│                                         │
└─────────────────────────────────────────┘
```

### Dockerfile Execution Flow

```
1. START: python:3.11-slim image
   ↓
2. Set environment variables
   ↓
3. Install Python dependencies
   ↓
4. Copy application code
   ↓
5. Create non-root user
   ↓
6. Expose port 5000
   ↓
7. Run: python app.py
   ↓
8. Flask listens on 0.0.0.0:5000
   ↓
9. Container ready for connections
```

---

## 🛡️ Security Best Practices Implemented

1. **Non-root User** - App runs as 'appuser' (not root)
   - Prevents container escape vulnerability
   
2. **Minimal Base Image** - `python:3.11-slim`
   - Only 130MB (vs 900MB for full Python)
   - Fewer packages = smaller attack surface
   
3. **Virtual Environment** - Dependencies isolated
   - System Python not modified
   - Easy cleanup
   
4. **Multi-stage Build** - Final image small and clean
   - Build tools not included
   - Reduced image size and vulnerabilities
   
5. **Health Check** - Monitors service health
   - Docker can auto-restart if unhealthy
   
6. **.dockerignore** - Excludes sensitive files
   - No .git, __pycache__, .env

---

## ⚠️ Troubleshooting

### Port 5000 Already in Use

```bash
# Find process using port 5000
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Mac/Linux

# Stop the running container
docker stop student-manager

# Or use a different port
docker run -d -p 5001:5000 smart-student-manager:latest
```

### "Cannot find module" Error

```bash
# Rebuild the image
docker build --no-cache -t smart-student-manager:latest .
```

### Database Issues

```bash
# Remove container and rebuild
docker rm student-manager
docker run -d -p 5000:5000 smart-student-manager:latest

# Database will be recreated on first run
```

### View Error Logs

```bash
docker logs student-manager
docker logs -f student-manager  # Follow logs
```

---

## 🚀 Production Deployment

For production, modify the Dockerfile:

```dockerfile
# Change debug mode
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# Add gunicorn to requirements.txt
gunicorn==20.1.0
```

Then build:
```bash
docker build -t smart-student-manager:prod .
docker run -d -p 5000:5000 smart-student-manager:prod
```

---

## 📈 Performance Tips

1. **Use .dockerignore** ✓ Already configured
2. **Multi-stage build** ✓ Already implemented
3. **Cache layers** - Put changing code last
4. **Minimal base image** ✓ Using slim variant

---

## 🎯 Summary

| Task | Command |
|------|---------|
| **Quick Start** | `docker-compose up` |
| **Build Image** | `docker build -t smart-student-manager:latest .` |
| **Run Container** | `docker run -d -p 5000:5000 --name student-manager smart-student-manager:latest` |
| **Stop Container** | `docker stop student-manager` |
| **View Logs** | `docker logs -f student-manager` |
| **Remove All** | `docker compose down && docker rmi smart-student-manager:latest` |

---

## 🔗 Useful Links

- **Docker Documentation**: https://docs.docker.com/
- **Docker Hub**: https://hub.docker.com/
- **Flask in Containers**: https://flask.palletsprojects.com/en/2.3.x/

---

**Created:** March 2024
**Docker Version:** 4.25+
**Python Version:** 3.11
