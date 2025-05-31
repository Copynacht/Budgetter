# Budgetter API Server Setup Guide

This API Server is built using Django. Follow the instructions below to set up your development environment and run the project locally.

## Setup Instructions

### 1. Create and Activate a Virtual Environment

```bash
python -m venv .venv
```

- On **Windows**:

```bash
.venv\Scripts\activate
```

- On **macOS/Linux**:

```bash
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file based on `.env.example`.

```bash
cp .env.example .env  # macOS/Linux

# Or manually copy `.env.example` to `.env` on Windows
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

## Environment

- Python 3.13.3
- Django (see `requirements.txt` for the specific version)
