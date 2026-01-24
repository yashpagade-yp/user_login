# User Management App

This repository contains a beginner-level User Management API project.
It is intended for students learning how to build their first API server using Python and FastAPI.

---

## Technology Stack

- Python 3.10 or above
- FastAPI
- Uvicorn
- Virtual Environment (venv)
- Git

---

## Prerequisites

Verify installations:

python --version  
git --version

---

## Virtual Environment Setup (Windows)

Create virtual environment:

python -m venv venv

Activate virtual environment (PowerShell):

venv\Scripts\activate

---

## Install Dependencies

Make sure requirements.txt exists, then run:

pip install -r requirements.txt

---

## Run the Server

Start the development server:

uvicorn app.main:app --reload

Server URL:

http://127.0.0.1:8000

API Documentation:

http://127.0.0.1:8000/docs  
http://127.0.0.1:8000/redoc

---

## Project Structure (Reference)

user-management-app/
│
├── app/
│   ├── main.py
│   ├── routers/
│   ├── models/
│   └── schemas/
│
├── requirements.txt
├── README.md
└── .gitignore

---

## Student Practice Rules

This project is strictly for learning and practice.

1. Do not work on the main branch.
2. Create a branch with your own name:

git checkout -b your-name

3. All code must be pushed to your own branch only.
4. Make small, meaningful commits.
5. Understand the code before writing or copying it.
6. Follow proper project structure.
7. Broken or untested code should not be pushed.

---

## Git Workflow

Add changes:

git add .

Commit changes:

git commit -m "Describe your change"

Push to your branch:

git push origin your-name

---

## Learning Goals

- Understanding API servers
- FastAPI fundamentals
- CRUD operations
- Request and response handling
- Python project structure
- Virtual environments
- Git branching and collaboration

---

## Restrictions

- No direct push to main branch
- No copying complete solutions
- No skipping virtual environment setup

---

## Note

This repository is for educational purposes only.
Focus on learning concepts, not completing quickly.
