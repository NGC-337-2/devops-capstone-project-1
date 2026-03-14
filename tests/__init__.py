"""
Test package initialization.
Set up testing environment before importing the app.
"""
import os

# Set testing environment before any app imports
os.environ["FLASK_ENV"] = "testing"
os.environ["DATABASE_URI"] = "sqlite:///:memory:"
