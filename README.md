# SafeRoute AI

A Flask backend for SafeRoute AI, an AI-assisted walking route recommender that fuses context, community incidents, and real-time environmental observations.

## Features
- Flask application factory pattern
- MongoDB incident ingestion and retrieval
- OSRM routing candidate generation
- OpenCV brightness scoring
- YOLOv8 crowd estimation
- Rule-based safety scoring and optimization

## Setup
1. Create a Python virtual environment: `python -m venv .venv`
2. Activate it: `.\.venv\Scripts\Activate.ps1` or `.\.venv\Scripts\activate.bat`
3. Install dependencies: `pip install -r req.txt`
4. Copy `.env.example` to `.env` and update settings.
5. Start the app: `python -m src.app`
