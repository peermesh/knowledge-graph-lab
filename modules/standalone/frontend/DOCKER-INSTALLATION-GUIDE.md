# Docker Desktop Installation Guide for Windows 11
## Complete Step-by-Step Instructions

**System Information:**
- OS: Windows 11 Home (Build 26200)
- CPU: Intel Core i7-10700K @ 3.80GHz (16 cores)
- RAM: ~16GB
- System Type: x64-based PC

**Status:** ✅ System meets all Docker requirements

---

## 📋 PHASE 1: Enable WSL 2 (Windows Subsystem for Linux)

### Why WSL 2?
Windows 11 Home edition requires WSL 2 as the backend for Docker Desktop (Hyper-V is only available in Pro/Enterprise editions). WSL 2 provides better performance and is the recommended option.

### Step 1: Enable WSL (Run PowerShell as Administrator)

**Important:** Right-click PowerShell and select "Run as Administrator"

```powershell
# Install WSL with default Ubuntu distribution
wsl --install

# This command will:
# - Enable Windows Subsystem for Linux
# - Enable Virtual Machine Platform
# - Download and install Ubuntu
# - Set WSL 2 as the default version
```

**Expected Output:**
```
Installing: Windows Subsystem for Linux
Windows Subsystem for Linux has been installed.
Installing: Ubuntu
Ubuntu has been installed.
The requested operation is successful. Changes will not be effective until the system is rebooted.
```

### Step 2: Restart Your Computer

**IMPORTANT:** You MUST restart Windows after this step.

```powershell
# Option 1: Restart via PowerShell
Restart-Computer

# Option 2: Restart via Start Menu
# Start Menu > Power > Restart
```

### Step 3: Verify WSL Installation (After Restart)

Open PowerShell (normal mode, not admin) and run:

```powershell
# Check WSL status
wsl --status

# Expected output should show:
# Default Distribution: Ubuntu
# Default Version: 2

# List installed distributions
wsl --list --verbose

# Expected output:
# NAME      STATE         VERSION
# Ubuntu    Stopped       2
```

### Step 4: Update WSL (Recommended)

```powershell
# Update WSL to the latest version
wsl --update

# Check version
wsl --version
```

---

## 📥 PHASE 2: Download Docker Desktop

### Step 1: Download Docker Desktop Installer

**Option A: Direct Download Link**
```
https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
```

**Option B: Official Website**
1. Go to: https://www.docker.com/products/docker-desktop/
2. Click "Download for Windows"
3. Save the installer (approximately 600MB)

### Step 2: Verify Download

Check the file location:
```powershell
# Usually downloads to:
C:\Users\simps\Downloads\Docker Desktop Installer.exe
```

---

## 🔧 PHASE 3: Install Docker Desktop

### Step 1: Run the Installer

1. **Double-click** `Docker Desktop Installer.exe`
2. **User Account Control** will prompt - Click "Yes"

### Step 2: Configuration Options

When the installer starts, you'll see configuration options:

**✅ CHECK THIS OPTION:**
```
☑ Use WSL 2 instead of Hyper-V (recommended)
```

**OPTIONAL:**
```
☐ Add shortcut to desktop
```

### Step 3: Wait for Installation

The installer will:
1. Extract files (~5 minutes)
2. Install Docker components
3. Configure WSL 2 integration

**Progress indicators:**
- Extracting files...
- Installing Docker Engine...
- Setting up WSL 2 backend...
- Configuring Docker Compose...

### Step 4: Complete Installation

When prompted:
```
Installation succeeded
Click "Close" to finish
```

**Do NOT start Docker Desktop yet** - we'll do that in the next phase.

---

## 🚀 PHASE 4: Initial Docker Desktop Setup

### Step 1: Launch Docker Desktop

1. **Start Menu** > Search for "Docker Desktop"
2. Click to launch (first launch takes 2-3 minutes)

### Step 2: Accept License Agreement

Docker Desktop will present the Docker Subscription Service Agreement:
- Read the agreement
- Click "Accept" to continue

### Step 3: Configuration Survey (Optional)

Docker may ask about your usage:
- **What do you want to use Docker for?** → "Development"
- **What's your experience level?** → Choose your level
- You can skip this if desired

### Step 4: Wait for Docker to Start

You'll see the Docker Desktop window with status:
```
Starting Docker Desktop...
Starting WSL 2 backend...
Docker Engine starting...
```

**Wait for:**
```
✅ Docker Desktop is running
```

This appears in the bottom-left corner. The Docker whale icon in your system tray should also be steady (not animated).

---

## ✅ PHASE 5: Verify Installation

### Step 1: Open PowerShell (New Window)

Open a **NEW** PowerShell window (not the old one).

### Step 2: Check Docker Version

```powershell
docker --version
```

**Expected Output:**
```
Docker version 24.x.x, build xxxxxxx
```

### Step 3: Check Docker Compose

```powershell
docker compose version
```

**Expected Output:**
```
Docker Compose version v2.x.x
```

### Step 4: Test Docker Installation

```powershell
# Run the hello-world container
docker run hello-world
```

**Expected Output:**
```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
...
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

### Step 5: Check Docker Status

```powershell
docker info
```

This should show detailed Docker configuration without errors.

---

## 🎯 PHASE 6: Test with Your Frontend Project

Now let's test Docker with your actual project!

### Step 1: Navigate to Frontend Directory

```powershell
cd C:\Users\simps\work\knowledge-graph-lab-new\frontend
```

### Step 2: Verify Docker Files

```powershell
# Check Dockerfile exists
Test-Path .\Dockerfile

# Check docker-compose.yml exists
Test-Path .\docker-compose.yml

# Both should return: True
```

### Step 3: Build and Run Frontend

```powershell
# Build and start the container
docker compose up -d
```

**Expected Output:**
```
[+] Building 120.5s (12/12) FINISHED
[+] Running 2/2
 ✔ Network knowledge-graph-lab-network  Created
 ✔ Container kg-lab-frontend            Started
```

### Step 4: Verify Container is Running

```powershell
# Check running containers
docker ps
```

**Expected Output:**
```
CONTAINER ID   IMAGE              COMMAND                  STATUS         PORTS
abc123def456   frontend-frontend  "nginx -g 'daemon of…"   Up 10 seconds  0.0.0.0:80->80/tcp
```

### Step 5: Test the Application

Open your browser and go to:
```
http://localhost
```

You should see the Knowledge Graph Lab frontend!

### Step 6: Check Health Status

```powershell
# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}"
```

**Expected Status:**
```
NAMES              STATUS
kg-lab-frontend    Up X minutes (healthy)
```

### Step 7: View Logs (If Needed)

```powershell
# View container logs
docker compose logs -f

# Press Ctrl+C to exit log view
```

---

## 🛑 PHASE 7: Docker Management Commands

### Essential Commands

```powershell
# Stop the frontend container
docker compose down

# Start the frontend container
docker compose up -d

# Restart the container
docker compose restart

# View logs
docker compose logs -f

# Check container status
docker ps

# Check all containers (including stopped)
docker ps -a

# Remove all stopped containers
docker container prune

# Check disk usage
docker system df

# Clean up unused resources (careful!)
docker system prune
```

---

## 🔧 TROUBLESHOOTING

### Issue 1: "WSL 2 installation is incomplete"

**Solution:**
```powershell
# Update WSL kernel
wsl --update

# Set WSL 2 as default
wsl --set-default-version 2

# Restart Docker Desktop
```

### Issue 2: Docker Desktop Won't Start

**Solution:**
```powershell
# 1. Close Docker Desktop completely
# 2. Open Task Manager (Ctrl+Shift+Esc)
# 3. End all Docker processes
# 4. Restart Docker Desktop
```

**Alternative:**
```powershell
# Restart Docker service (run as Administrator)
Get-Service com.docker.service | Restart-Service
```

### Issue 3: "Error response from daemon"

**Solution:**
```powershell
# 1. Check if Docker Desktop is running (system tray icon)
# 2. Restart Docker Desktop
# 3. Try the command again
```

### Issue 4: Port 80 Already in Use

**Solution:**
```powershell
# Check what's using port 80
netstat -ano | findstr :80

# Change the port in docker-compose.yml:
# From: "80:80"
# To:   "8080:80"

# Then access at: http://localhost:8080
```

### Issue 5: Virtualization Not Enabled

**Error Message:**
```
Hardware assisted virtualization and data execution protection must be enabled in the BIOS
```

**Solution:**
1. Restart computer
2. Enter BIOS setup (press F2, F10, Del, or Esc during boot)
3. Find "Virtualization Technology" or "Intel VT-x"
4. Enable it
5. Save and exit BIOS
6. Restart Docker Desktop

### Issue 6: Slow Performance

**Optimization Tips:**
```powershell
# 1. Allocate more resources to Docker
# Docker Desktop > Settings > Resources
# - CPUs: 4-8 cores (you have 16 available)
# - Memory: 4-8 GB (you have 16 GB available)

# 2. Limit disk usage
# Docker Desktop > Settings > Resources > Disk image size
# Set to 64GB (default)

# 3. Enable resource usage limits
# Docker Desktop > Settings > Resources > Advanced
```

---

## 📊 CONFIGURATION RECOMMENDATIONS

### Docker Desktop Settings

**1. Resources (Recommended for Your System):**
```
CPUs: 6-8 (of your 16 cores)
Memory: 6-8 GB (of your 16 GB)
Swap: 2 GB
Disk image size: 64 GB
```

**2. General:**
```
☑ Start Docker Desktop when you log in (optional)
☐ Send usage statistics (optional)
☑ Use the WSL 2 based engine
```

**3. WSL Integration:**
```
☑ Enable integration with my default WSL distro
☑ Ubuntu (if you want to use Docker from Ubuntu terminal)
```

**4. Docker Engine (Advanced):**
```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "features": {
    "buildkit": true
  }
}
```

---

## 📚 USEFUL DOCKER COMMANDS

### Container Management

```powershell
# List running containers
docker ps

# List all containers
docker ps -a

# Stop a container
docker stop <container-id>

# Remove a container
docker rm <container-id>

# Remove all stopped containers
docker container prune
```

### Image Management

```powershell
# List images
docker images

# Remove an image
docker rmi <image-id>

# Remove unused images
docker image prune

# Build an image
docker build -t myapp .
```

### Docker Compose Commands

```powershell
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs

# Rebuild and start
docker compose up -d --build

# Stop and remove everything
docker compose down -v
```

### System Maintenance

```powershell
# Check disk usage
docker system df

# Clean up everything (careful!)
docker system prune -a

# View Docker info
docker info

# Check Docker version
docker version
```

---

## 🎓 NEXT STEPS AFTER INSTALLATION

### 1. Explore Docker Desktop Dashboard

- Click the Docker icon in system tray
- Click "Dashboard"
- You can see:
  - Running containers
  - Images
  - Volumes
  - Logs in real-time

### 2. Test Your Frontend Project

```powershell
cd C:\Users\simps\work\knowledge-graph-lab-new\frontend
docker compose up -d
```

Visit: http://localhost

### 3. Learn Docker Basics

**Key Concepts:**
- **Images**: Templates for containers (like a blueprint)
- **Containers**: Running instances of images (like a house built from blueprint)
- **Volumes**: Persistent data storage
- **Networks**: Communication between containers

### 4. Monitor Resources

```powershell
# View container resource usage
docker stats

# Press Ctrl+C to exit
```

---

## 📞 GETTING HELP

### Official Resources

- **Docker Documentation**: https://docs.docker.com/
- **Docker Desktop Manual**: https://docs.docker.com/desktop/
- **WSL Documentation**: https://docs.microsoft.com/en-us/windows/wsl/

### Community Support

- **Docker Forums**: https://forums.docker.com/
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/docker
- **Docker Slack**: https://dockercommunity.slack.com/

---

## ✅ INSTALLATION CHECKLIST

Use this checklist to track your progress:

- [ ] Phase 1: Enable WSL 2
  - [ ] Run `wsl --install`
  - [ ] Restart computer
  - [ ] Verify WSL with `wsl --status`

- [ ] Phase 2: Download Docker Desktop
  - [ ] Downloaded installer (600MB)

- [ ] Phase 3: Install Docker Desktop
  - [ ] Ran installer
  - [ ] Selected "Use WSL 2"
  - [ ] Installation completed

- [ ] Phase 4: Initial Setup
  - [ ] Launched Docker Desktop
  - [ ] Accepted license
  - [ ] Docker Desktop running

- [ ] Phase 5: Verify Installation
  - [ ] `docker --version` works
  - [ ] `docker compose version` works
  - [ ] `docker run hello-world` succeeds

- [ ] Phase 6: Test Frontend
  - [ ] `docker compose up -d` succeeds
  - [ ] Container is running (`docker ps`)
  - [ ] Application accessible at http://localhost
  - [ ] Health check passes

- [ ] Phase 7: Cleanup
  - [ ] Know how to stop: `docker compose down`
  - [ ] Know how to view logs: `docker compose logs -f`

---

## 🎉 COMPLETION

Once all checklist items are complete, you have successfully installed Docker Desktop and deployed your frontend module!

**Your frontend is Docker-ready and production-capable!**

---

**Created:** 2024
**Last Updated:** Based on Docker Desktop 4.x and WSL 2
**For:** Knowledge Graph Lab Frontend Module
**System:** Windows 11 Home (Build 26200)


