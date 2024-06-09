from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from confluent_kafka import Producer
import json

from models import Base, TodoItem, SessionLocal, engine

app = FastAPI()

KAFKA_TOPIC = "todo_topic"
KAFKA_SERVER = "localhost:9092"

p = Producer({'bootstrap.servers': KAFKA_SERVER})

class TodoItemCreate(BaseModel):
    title: str
    description: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/todo/")
def create_todo_item(item: TodoItemCreate, db: Session = Depends(get_db)):
    db_item = TodoItem(title=item.title, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    p.produce(KAFKA_TOPIC, key=str(db_item.id), value=json.dumps(item.dict()))
    return db_item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
