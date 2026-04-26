# 🖥️ System Monitor

### Real-Time System Monitoring & Process Management Dashboard

---

## 📌 Overview

**System Monitor** is a desktop-based system monitoring tool built using Python and PySide6. It provides real-time insights into system performance, including CPU usage, memory consumption, disk activity, and network statistics.

The application also includes a process management module that allows users to monitor, filter, and control running processes efficiently—similar to a modern Task Manager.

---

## 🎯 Features

### 📊 Performance Monitoring

* Real-time CPU usage (with per-core visualization)
* Memory usage tracking
* Disk usage statistics
* Network activity (upload/download)
* Circular gauges and live sparkline graphs

### 🔧 Process Management

* View all running processes
* Search and filter by name or PID
* Sort processes by CPU, memory, threads, etc.
* Kill or terminate processes
* Suspend and resume processes (Linux)

### 👤 User Monitoring

* Display currently logged-in users
* Session details (terminal, host, start time)

### 🎨 UI/UX Highlights

* Modern dark theme dashboard
* Color-coded metrics (green, yellow, red)
* Interactive tables and real-time updates
* Smooth animations and custom widgets

---

## 🧠 Key Concepts Used

* Process Management
* CPU Scheduling & Utilization
* Memory Management
* Multi-threading (QThread)
* Real-time Data Visualization

---

## 🛠️ Technologies Used

### Programming Language

* Python

### Libraries & Frameworks

* PySide6 (GUI Framework)
* psutil (System Monitoring)
* subprocess (System-level commands)

### Tools

* Git & GitHub (Version Control)

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/jaganmohanreddymandli/processmonitor.git
cd processmonitor
python -m venv venv
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python tm.py
```

---

## 🔐 Run with Administrator (Recommended)

### Windows:

* Open Command Prompt → Run as Administrator
* Then run:

```bash
python tm.py
```

### Or Auto-Elevate (Optional):

Add admin privilege code using `ctypes` in Python.

---

## ⚠️ Important Notes

* CPU usage may exceed 100% because it is calculated across multiple CPU cores.
* "System Idle Process" represents unused CPU (higher = better performance).
* Some system processes cannot be terminated due to OS protection.

---

## 🚀 Future Enhancements

* GPU monitoring support
* Process priority control
* Alert system for high CPU/memory usage
* Export logs (CSV/JSON)
* Light/Dark theme toggle

---

## 📷 Screenshots

(Add your screenshots here)

---

## 📚 References

* Python Documentation
* psutil Documentation
* PySide6 Documentation
* GeeksforGeeks (Operating Systems)

---

## 👨‍💻 Authors

* Jaganmohan Reddy, Nithin, Nishar
* Course: CSE316 - Operating Systems
* Lovely Professional University

---

## 📄 License

This project is for academic purposes only.
