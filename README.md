# FastAPI + Next.js Scaffold

This project is a monorepo containing a FastAPI backend and a Next.js frontend.

## Project Structure

- `./backend`: FastAPI application with SQLAlchemy and Pydantic.
- `./frontend`: Next.js application with Tailwind CSS and TypeScript.

## Quick Start

### 1. Prerequisites
- Node.js (v18+)
- Python (3.9+)

### 2. Installation
Install both frontend and backend dependencies:
```bash
npm run install:all
```

### 3. Running the Application
You can run both the frontend and backend simultaneously using:
```bash
npm run dev
```

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Separate Commands

### Backend Only
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

### Frontend Only
```bash
cd frontend
npm run dev
```

## Testing
To run backend tests:
```bash
npm run test:backend
```
