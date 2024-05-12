"""
Main entry point for FastAPI
"""
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    """
    root endpoint
    """
    return "Welcome to Resume NLP!"
