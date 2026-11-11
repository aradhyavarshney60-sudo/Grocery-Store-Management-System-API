# Grocery Store Management System - REST API

A production-ready RESTful backend built with Python, Django REST Framework (DRF), SimpleJWT, and SQLite for grocery store operations.

## Features
- **JWT Authentication:** Secure user signup and token-based login (`/api/register/`, `/api/login/`).
- **Role-Based Access Control:** Separate roles for `Customer`, `Admin`, and `DeliveryStaff`.
- **Item Inventory Management:** Full CRUD on grocery items with category/brand filtering, search, and pagination.
- **Order Processing:** Multi-item cart checkout with dynamic inventory reduction, delivery tracking, and status transitions.
- **OpenAPI & Swagger Documentation:** Interactive API documentation hosted at `/api/docs/`.

## Setup & Running
```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver