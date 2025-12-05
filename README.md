# The Energy Red (AI Energy Manager)

This project is an AI-powered energy management system designed to monitor, analyze, and optimize energy consumption.

## Features
- **Real-time Monitoring**: Fetches energy data from Abysis API.
- **Anomaly Detection**: Detects voltage imbalances and other irregularities.
- **AI Integration**: Uses OpenAI to analyze data and provide insights.
- **Dashboard**: FastAPI-based backend for serving data to the frontend.

## Tech Stack
- **Backend**: Python, FastAPI
- **Database**: PostgreSQL (TimescaleDB)
- **Task Queue**: Celery + Redis
- **Containerization**: Docker & Docker Compose

## Setup
1. Clone the repository.
2. Create a `.env` file with necessary credentials.
3. Run `docker-compose up --build`.
