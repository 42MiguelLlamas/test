from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("API_KEY", "123456")  # default dev key

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "inbound_api.db"

# Middleware para verificar API Key
@app.middleware("http")
async def check_api_key(request: Request, call_next):
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return await call_next(request)

# Endpoint GET /search_loads
@app.get("/search_loads")
def search_loads(equipment_type: str = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if equipment_type:
        cursor.execute("SELECT * FROM loads WHERE equipment_type = ? LIMIT 1", (equipment_type,))
    else:
        cursor.execute("SELECT * FROM loads LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "load_id": row[0],
            "origin": row[1],
            "destination": row[2],
            "pickup_datetime": row[3],
            "delivery_datetime": row[4],
            "equipment_type": row[5],
            "loadboard_rate": row[6],
            "notes": row[7],
        }
    return {"message": "No load found"}

# Modelo para POST /log_call_result
class CallLog(BaseModel):
    mc_number: str
    load_id: str
    final_rate: int
    outcome: str
    sentiment: str
    negotiation_rounds: int
    timestamp: str = datetime.utcnow().isoformat()

@app.post("/log_call_result")
def log_call_result(log: CallLog):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO call_logs (mc_number, load_id, final_rate, outcome, sentiment, negotiation_rounds, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (log.mc_number, log.load_id, log.final_rate, log.outcome, log.sentiment, log.negotiation_rounds, log.timestamp))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Call log saved."}
