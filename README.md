# Backend

This directory contains the Flask backend for the Attendance System.

## Setup

1. Install Python 3.9+.
2. Create a virtual environment: `python -m venv venv`.
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`.
5. Create a `.env` file with the following variables:
   ```
   DB_HOST=...
   DB_NAME=...
   DB_USER=...
   DB_PASSWORD=...
   SUPABASE_URL=...
   SUPABASE_KEY=...
   SECRET_KEY=...
   JWT_SECRET_KEY=...
   ```
6. Run the server: `python run.py`.

## Deployment

This project is configured for deployment on Render using `render.yaml`.

## API Documentation

- Swagger UI: `http://localhost:5000/swagger-ui`
