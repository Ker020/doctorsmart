# Smart Healthcare System

## Overview

Smart Healthcare System is an AI-powered healthcare web application developed using Flask, MariaDB, Gunicorn, Nginx, and Ollama. The application provides an intelligent medical assistant that runs locally using a Large Language Model (LLM), making it suitable for offline or private healthcare environments.

---

# Features

* Patient Management
* Doctor Dashboard
* AI Medical Assistant
* Local AI using Ollama
* Secure Authentication
* Flask Backend
* MariaDB Database
* Gunicorn Application Server
* Nginx Reverse Proxy

---

# Project Structure

```text
source-code/
│
├── app/
├── run.py
├── wsgi.py
└── smart_healthcare.sql
```

---

# System Requirements

The project has been tested on:

* Debian 12 or later
* Python 3.10+
* MariaDB Server
* Nginx
* Ollama
* Git

---

# Installation Guide

## Step 1 – Update the System

```bash
sudo apt update
sudo apt upgrade -y
```

---

## Step 2 – Install Required Packages

```bash
sudo apt install -y \
python3 \
python3-pip \
python3-venv \
mariadb-server \
nginx \
git \
curl \
unzip
```

---

## Step 3 – Copy Project Files

Extract the project into:

```text
/var/www/html/smart_healthcare_web/
```

---

## Step 4 – Create Python Virtual Environment

```bash
cd /var/www/html/smart_healthcare_web

python3 -m venv /home/<USERNAME>/my_env

source /home/<USERNAME>/my_env/bin/activate
```

Install the project dependencies using the attached requirements file.

```bash
pip install -r requirements.txt
pip install gunicorn
```

---

## Step 5 – Configure MariaDB

Create the database:

```sql
CREATE DATABASE smart_healthcare CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Import the database:

```bash
mysql -u root -p smart_healthcare < smart_healthcare.sql
```

---

## Step 6 – Install Ollama

Install Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Download the required AI model:

```bash
ollama pull qwen2.5:7b
```

Verify installation:

```bash
ollama list
```

---

## Step 7 – Configure the Application

Before running the application, update the project configuration files to match your server environment.

### 1. Environment Variables

Edit either:

```text
.env
```

or

```text
.env.production
```

depending on the deployment environment.

Update the following values:

* `SECRET_KEY`
* `DATABASE_URL`
* `GOOGLE_MAPS_API_KEY` *(optional)*
* `GOOGLE_PLACES_KEY` *(optional)*
* Any additional environment variables required by your deployment.

---

### 2. Application Configuration

Open:

```text
app/config.py
```

Review and update the following settings if they are not being loaded from the environment variables:

* Database connection
* Default `SECRET_KEY`
* AI model configuration (`LLM_MODEL`)
* AI server URL (`LLM_API_URL`)
* Upload directory (if changed)
* Google Maps API configuration (if used)

> **Note:** It is recommended to configure the application using environment variables instead of hardcoding sensitive information inside `config.py`.

---

### 3. Systemd Service

The project includes a preconfigured service file named:

```text
smart-healthcare.service
```

Copy it to the systemd directory:

```bash
sudo cp smart-healthcare.service /etc/systemd/system/
```

Before starting the service, edit the file and update the following values to match your server configuration:

* Python virtual environment path
* Project working directory
* Database credentials
* Database name
* Secret Key
* Ollama model name (if different)
* Ollama API URL (if different)

Reload systemd:

```bash
sudo systemctl daemon-reload
```

Enable the service:

```bash
sudo systemctl enable smart-healthcare
```

Start the application:

```bash
sudo systemctl start smart-healthcare
```

Verify that the service is running correctly:

```bash
sudo systemctl status smart-healthcare
```

> **Important:** Before starting the service, edit `smart-healthcare.service` , `.env` , `.env.production` and update the following values to match your environment:
>
> * Database password
> * Secret Key
> * Python virtual environment path
> * Working directory (if different)

---

## Step 8 – Configure Nginx

A ready-to-use Nginx configuration file (`nginx.conf`) is included with the project.

Copy it:

```bash
sudo cp nginx.conf /etc/nginx/sites-available/smart-healthcare
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/smart-healthcare /etc/nginx/sites-enabled/
```

Test the configuration:

```bash
sudo nginx -t
```

Restart Nginx:

```bash
sudo systemctl restart nginx
```

---

## Step 9 – Verify Services

Ensure all required services are running:

```bash
sudo systemctl status mariadb

sudo systemctl status ollama

sudo systemctl status nginx

sudo systemctl status smart-healthcare
```

---

## Access the Application

Open your browser and navigate to:

```text
http://SERVER_IP
```

or

```text
http://YOUR_DOMAIN
```

---

# Included Files

The following configuration files are already included with the project:

* `requirements.txt` — Python package dependencies.
* `smart-healthcare.service` — Systemd service configuration.
* `nginx.conf` — Nginx reverse proxy configuration.
* `smart_healthcare.sql` — Database schema and initial data.

---

# Troubleshooting

### View application logs

```bash
sudo journalctl -u smart-healthcare -f
```

### View Nginx logs

```bash
sudo tail -f /var/log/nginx/error.log
```

### Verify Ollama

```bash
curl http://127.0.0.1:11434/api/tags
```

---

# Notes

* Make sure MariaDB, Ollama, Gunicorn, and Nginx are running before accessing the application.
* Update the values inside `smart-healthcare.service` before deployment.
* The AI model must be downloaded successfully before the application starts.
* This project is intended to run on Ubuntu Linux using Gunicorn and Nginx.