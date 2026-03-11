# DevOps Capstone Project - Account Service

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-green.svg)
![Flask](https://img.shields.io/badge/Flask-2.1.2-orange.svg)

A production-ready Flask REST API microservice for managing user accounts, demonstrating modern DevOps practices including containerization, Kubernetes orchestration, and CI/CD pipelines with Tekton.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Tekton CI/CD Pipeline](#tekton-cicd-pipeline)
- [Makefile Commands](#makefile-commands)
- [License](#license)

## Overview

This is a DevOps capstone project that showcases a complete software development lifecycle including:

- **REST API Development**: Flask-based microservice for account management
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **Containerization**: Docker images for the application
- **Orchestration**: Kubernetes (K3d) for container management
- **CI/CD Automation**: Tekton pipelines for continuous integration and deployment
- **Testing**: Comprehensive unit tests with code coverage
- **Code Quality**: Linting, formatting, and security scanning

## Features

- ✅ RESTful API with standard HTTP methods
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Security headers via Flask-Talisman
- ✅ CORS support for cross-origin requests
- ✅ Health check endpoint for container orchestration
- ✅ Comprehensive error handling
- ✅ Unit tests with code coverage reporting
- ✅ Docker containerization
- ✅ Kubernetes deployment manifests
- ✅ Tekton CI/CD pipeline definitions

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.9+ |
| Framework | Flask 2.1.2 |
| Database | PostgreSQL |
| ORM | SQLAlchemy 1.4.46 |
| WSGI Server | Gunicorn 20.1.0 |
| Container | Docker |
| Orchestration | Kubernetes (K3d) |
| CI/CD | Tekton |
| Testing | nose, factory-boy |
| Code Quality | pylint, flake8, black |

## Project Structure

```
devops-capstone-project/
├── .devcontainer/          # Dev Container configuration
├── .github/                # GitHub workflows (if any)
├── bin/                    # Setup and utility scripts
├── deploy/                # Kubernetes deployment manifests
├── service/               # Main application code
│   ├── __init__.py        # Flask app initialization
│   ├── config.py          # Application configuration
│   ├── models.py          # Database models
│   ├── routes.py          # API route handlers
│   └── common/            # Common utilities (error handlers, logging)
├── tekton/                # Tekton pipeline definitions
│   ├── pipeline.yaml      # Pipeline definition
│   ├── tasks.yaml         # Task definitions
│   └── pvc.yaml           # Persistent Volume Claim
├── tests/                 # Unit tests
│   ├── test_accounts.py  # API endpoint tests
│   ├── test_models.py    # Model tests
│   └── factories.py      # Test factories
├── .flaskenv              # Flask configuration
├── .gitignore             # Git ignore patterns
├── Makefile               # Development automation
├── Procfile               # Gunicorn startup command
├── requirements.txt       # Python dependencies
└── setup.cfg              # Tool configurations
```

## Prerequisites

- Python 3.9 or higher
- Docker
- Kubernetes (K3d) or Minikube
- Tekton CLI (`tkn`)
- PostgreSQL (local or containerized)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd devops-capstone-project
```

### 2. Create Virtual Environment

```bash
# Using make
make venv

# Or manually
python3 -m venv ~/venv
source ~/venv/bin/activate  # Linux/Mac
# or
~/venv/Scripts/activate  # Windows
```

### 3. Install Dependencies

```bash
make install
```

Or manually:

```bash
pip install --upgrade pip wheel
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL

```bash
# Using Docker
make db

# This will start PostgreSQL on port 5432
```

### 5. Configure Environment Variables

Create a `.env` file or set environment variables:

```bash
export DATABASE_URI="postgresql://postgres:postgres@localhost:5432/postgres"
export SECRET_KEY="your-secret-key"
```

## Running the Application

### Development Mode (with Honcho)

```bash
make run
# or
honcho start
```

The service will start on `http://localhost:8000`

### Production Mode (with Gunicorn)

```bash
gunicorn --workers=1 --bind 0.0.0.0:$PORT --log-level=info service:app
```

### Using Docker

```bash
# Build the image
make build

# Push to K3d registry
make push
```

## Running Tests

```bash
# Run all tests with coverage
make tests

# Run specific test file
nosetests -vv tests/test_accounts.py

# Run with coverage report
nosetests -vv --with-coverage --cover-package=service tests/
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page |
| GET | `/health` | Health check |
| GET | `/accounts` | List all accounts |
| GET | `/accounts/<id>` | Get account by ID |
| POST | `/accounts` | Create new account |
| PUT | `/accounts/<id>` | Update account |
| DELETE | `/accounts/<id>` | Delete account |

### Example: Create Account

```bash
POST /accounts
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com",
    "address": "123 Main Street",
    "phone_number": "555-1234"
}
```

### Example Response

```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "address": "123 Main Street",
    "phone_number": "555-1234",
    "date_joined": "2024-01-15"
}
```

## Kubernetes Deployment

### Create K3d Cluster

```bash
make cluster
```

This creates a K3d cluster with a local Docker registry on port 32000.

### Install Tekton

```bash
make tekton
make clustertasks
```

### Deploy Application

```bash
kubectl apply -f deploy/
```

### Verify Deployment

```bash
kubectl get pods
kubectl get services
```

## Tekton CI/CD Pipeline

The project includes Tekton pipeline definitions for continuous integration:

- **Pipeline**: `cd-pipeline` (defined in `tekton/pipeline.yaml`)
- **Tasks**: Git clone, linting, testing, building Docker images
- **Workspace**: Persistent volume for shared artifacts

### Apply Tekton Resources

```bash
kubectl apply -f tekton/pvc.yaml
kubectl apply -f tekton/tasks.yaml
kubectl apply -f tekton/pipeline.yaml
```

### Run Pipeline

```bash
tkn pipeline start cd-pipeline \
  --param repo-url=https://github.com/your-repo/devops-capstone-project.git \
  --workspace name=pipeline-workspace,claimName=pipelinerun-pvc
```

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make help` | Display help message |
| `make venv` | Create Python virtual environment |
| `make install` | Install Python dependencies |
| `make lint` | Run code linters |
| `make tests` | Run unit tests |
| `make run` | Start the service |
| `make db` | Start PostgreSQL container |
| `make dbrm` | Stop and remove PostgreSQL |
| `make cluster` | Create K3d Kubernetes cluster |
| `make tekton` | Install Tekton in cluster |
| `make build` | Build Docker image |
| `make push` | Push image to registry |

## Code Quality

The project uses multiple code quality tools:

### Linting

```bash
make lint
```

Runs flake8 with strict rules:
- No syntax errors
- No undefined names
- Maximum complexity: 10
- Maximum line length: 127

### Code Formatting

```bash
black .
```

### Security

- Flask-Talisman for security headers
- CORS configuration for controlled access
- SQLAlchemy ORM for SQL injection prevention


<p align="center">Built with ❤️ using Flask, Docker, Kubernetes, and Tekton</p>

