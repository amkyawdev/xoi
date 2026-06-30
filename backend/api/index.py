# Vercel Serverless Function Entry Point
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app

application = app
