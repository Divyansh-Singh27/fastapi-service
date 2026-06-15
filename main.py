from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FastAPI ECS Service", version="1.0.0")


class GreetResponse(BaseModel):
    message: str


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/about")
def about():
    return {
        "service": "FastAPI ECS Service",
        "version": "1.0.0",
        "description": "A simple FastAPI service running on AWS ECS Fargate",
        "author": "Divyansh Singh",
    }


@app.get("/greet")
def greet(name: str = "World"):
    return GreetResponse(message=f"Hello, {name}! Welcome to FastAPI on ECS Fargate.")
