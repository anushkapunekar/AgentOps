# AgentOps

A FastAPI-based backend service.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
agentops/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── routes/             # API route handlers
│   ├── __init__.py
│   └── example.py
├── utils/              # Utility functions
│   ├── __init__.py
│   └── helpers.py
└── models/             # Data models and schemas
    ├── __init__.py
    └── schemas.py
```

