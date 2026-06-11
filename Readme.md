# 🚀 ATS Resume Builder

An AI-powered ATS Resume Builder that helps optimize resumes for job descriptions and improves ATS (Applicant Tracking System) compatibility.

---
## 🎥 Project Demo

<p align="center">
  <a href="https://youtu.be/SnN-b_MQZWA">
    <img src="https://img.youtube.com/vi/SnN-b_MQZWA/maxresdefault.jpg" alt="ATS Resume Analyzer Demo" width="900">
  </a>
</p>

<p align="center">
 

---

## 📋 Prerequisites

Before starting, make sure you have:

* Linux (Ubuntu recommended)
* Internet connection
* Sudo privileges

---

## ⚡ Installation Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/vivekprajapati161632-ctrl/Ats_resume.git
```

### Step 2: Navigate to the Project Directory

```bash
cd Ats_resume
```

### Step 3: Make the Installation Script Executable

```bash
chmod +x docker.sh
```

### Step 4: Install Docker Automatically

```bash
./docker.sh
```

The script will automatically install Docker and configure the required dependencies.

---

## 🐳 Pull the Docker Image

After Docker installation is completed, pull the latest application image:

```bash
docker pull vivek3232/ats-resume:latest
```

---

## ▶️ Run the Application

```bash
docker run -d \
-p 8501:8501 \
--name ats-resume \
vivek3232/ats-resume:latest
```

---

## 🌐 Access the Application

Open your browser and visit:

```text
http://localhost:8501
```

Or replace `localhost` with your server's public IP address:

```text
http://YOUR_SERVER_IP:8501
```

---

## ✨ Features

* ATS-Friendly Resume Generation
* AI-Powered Resume Optimization
* Job Description Matching
* Modern User Interface
* Dockerized Deployment
* Easy Installation

---

## 📂 Project Structure

```text
Ats_resume/
├── docker.sh
├── Dockerfile
├── requirements.txt
├── app.py
└── README.md
```

---

## 🔧 Useful Docker Commands

### View Running Containers

```bash
docker ps
```

### View Logs

```bash
docker logs ats-resume
```

### Stop Container

```bash
docker stop ats-resume
```

### Remove Container

```bash
docker rm ats-resume
```

### Remove Image

```bash
docker rmi vivek3232/ats-resume:latest
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

Feel free to fork the repository and submit a pull request.

---

## 📜 License

This project is licensed under the MIT License.

---

### ⭐ Support

If you find this project useful, please consider giving it a **Star ⭐** on GitHub.
