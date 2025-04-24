from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import fetch_all_threats

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # React frontend URL
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/threats")
def get_threats():
    threats = fetch_all_threats()
    return [{
        "id": threat.id,
        "title": threat.title,
        "timestamp": threat.timestamp.isoformat(),
        "analysis": threat.analysis
    } for threat in threats]
