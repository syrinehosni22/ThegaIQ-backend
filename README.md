# ThegaIQ-backend

ThegaIQ-backend is a Flask backend application implementing **user management** with **role-based access control (RBAC)** extended by **capabilities** (fine-grained permissions).  
It supports both **HTML routes** and **JSON API routes**, enabling user authentication, role assignment, capability assignment, role hierarchy, and access enforcement via decorators.

---

## Table of Contents
- [Module Overview](#module-overview)  
- [Technology Stack](#technology-stack)    
- [Access Control Logic](#access-control-logic)  
- [Installation & Setup](#installation--setup)  
- [Configuration](#configuration)  
- [Usage](#usage)  
- [CLI Commands](#cli-commands)  
- [API Endpoints](#api-endpoints)  
- [Testing](#testing)   
- [License](#license)  

---

## Module Overview

This project implements a **user management backend** using Flask, with **role-based access control (RBAC)** enhanced by **capabilities** (fine-grained permissions).  

The system allows:
- User authentication and session management  
- Role assignment to users  
- Capability assignment to roles  
- Role hierarchy (parent-child roles)  
- Access enforcement using decorators  
- Support for both **HTML routes** and **JSON API routes**  

---

## Technology Stack

- **Backend Framework:** Flask (Python 3.10+)  
- **ORM:** SQLAlchemy  
- **Authentication:** Flask-Login  
- **Password Hashing:** Werkzeug (bcrypt/argon2)  
- **Database:** PostgreSQL (preferred) or MySQL  
- **Migrations:** Flask-Migrate (Alembic)  

---

## Access Control Logic

- Users may have **multiple roles**  
- Roles may inherit other roles via **parent_id**  
- Roles may have **multiple capabilities**  
- A user’s **effective capabilities** = direct + inherited role capabilities  

> Access to routes is enforced via decorators checking for required capabilities.

---

## Installation & Setup

1. **Clone the repository**  
```bash
git clone https://github.com/username/ThegaIQ-backend.git
cd ThegaIQ-backend
