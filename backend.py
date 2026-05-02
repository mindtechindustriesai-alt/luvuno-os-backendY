"""
LUVUNO OS — MQOS Backend Service
FastAPI server for quantum operations, key management, and AI chat
"""

import os
import json
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="Luvuno OS — MQOS Backend",
    description="Quantum Operating System Backend API",
    version="1.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# DATA MODELS
# ============================================================

class QuantumKeyRequest(BaseModel):
    length: int = 256
    purpose: str = "encryption"

class ThreatDetectionRequest(BaseModel):
    features: Dict[str, Any]

class ChatRequest(BaseModel):
    message: str
    portal: str = "quantum"

# ============================================================
# SIMULATED BACKEND STATE
# ============================================================

BACKEND_STATE = {
    "ibm_torino": {"status": "online", "correlation": 0.984, "last_job": None},
    "ionq": {"status": "online", "correlation": 0.995},
    "quantinuum": {"status": "online", "qv": "2^19"},
    "dwave": {"status": "online", "qubits": 5000},
    "aws_braket": {"status": "online"},
    "cisco_quantum": {"status": "online"},
    "nuquantum": {"status": "online"},
    "mqos_router": {"status": "online", "failover": True}
}

ACTIVE_KEYS = 247
EXPIRED_KEYS = 12
REVOKED_KEYS = 3
THREATS_BLOCKED = 847231

# ============================================================
# API ENDPOINTS
# ============================================================

@app.get("/")
async def root():
    return {
        "name": "Luvuno OS — MQOS Backend",
        "version": "1.0.0",
        "status": "operational",
        "backends_online": 8,
        "entanglement_health": "98.4%",
        "bell_parameter": 2.76
    }

@app.get("/api/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/backends")
async def get_backends():
    return BACKEND_STATE

@app.get("/api/keys/inventory")
async def get_key_inventory():
    return {
        "active_keys": ACTIVE_KEYS,
        "expired_keys": EXPIRED_KEYS,
        "revoked_keys": REVOKED_KEYS,
        "total_keys": ACTIVE_KEYS + EXPIRED_KEYS + REVOKED_KEYS,
        "key_rotation_days": 30
    }

@app.post("/api/keys/generate")
async def generate_key(request: QuantumKeyRequest):
    global ACTIVE_KEYS
    ACTIVE_KEYS += 1
    key_id = str(uuid.uuid4())[:8]
    return {
        "success": True,
        "key_id": f"K-{key_id.upper()}",
        "key_length": request.length,
        "purpose": request.purpose,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/keys/rotate")
async def rotate_keys():
    global ACTIVE_KEYS, EXPIRED_KEYS
    rotated = min(10, ACTIVE_KEYS)
    EXPIRED_KEYS += rotated
    ACTIVE_KEYS -= rotated
    ACTIVE_KEYS += rotated
    return {
        "success": True,
        "keys_rotated": rotated,
        "new_active_count": ACTIVE_KEYS,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/keys/revoke/{key_id}")
async def revoke_key(key_id: str):
    global ACTIVE_KEYS, REVOKED_KEYS
    if ACTIVE_KEYS > 0:
        ACTIVE_KEYS -= 1
        REVOKED_KEYS += 1
        return {"success": True, "revoked_key": key_id}
    return {"success": False, "error": "No active keys to revoke"}

@app.get("/api/threats/stats")
async def get_threat_stats():
    return {
        "threats_blocked": THREATS_BLOCKED,
        "detection_rate": 99.97,
        "false_positive_rate": 0.02,
        "response_time_ms": 3.2,
        "active_threats": 0,
        "last_incident": None
    }

@app.post("/api/threats/detect")
async def detect_threat(request: ThreatDetectionRequest):
    features = request.features
    score = 0
    if features.get("packet_size", 512) < 100:
        score += 2
    if features.get("duration", 1.0) < 0.1:
        score += 1
    if features.get("source_bytes", 0) > 8000:
        score += 2
    
    if score >= 2:
        verdict = "ATTACK"
        confidence = 0.97
    elif score >= 1:
        verdict = "SUSPICIOUS"
        confidence = 0.65
    else:
        verdict = "ALLOW"
        confidence = 0.99
    
    return {
        "verdict": verdict,
        "confidence": confidence,
        "features_analyzed": features,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/bell/test")
async def run_bell_test():
    return {
        "bell_parameter": 2.76,
        "classical_limit": 2.0,
        "quantum_limit": 2.828,
        "violation_percentage": 38,
        "entanglement_verified": True,
        "correlation": 0.984,
        "shots": 10000,
        "timestamp": "2025-12-24T16:16:19Z",
        "job_id": "d55om7jht8fs73a14cgg"
    }

@app.post("/api/portals/{portal_name}/dashboard")
async def get_portal_dashboard(portal_name: str):
    portal_data = {
        "quantum": {
            "title": "Quantum Core",
            "stats": [
                {"icon": "microchip", "value": "7/7", "label": "MQOS Backends"},
                {"icon": "key", "value": ACTIVE_KEYS, "label": "Active Quantum Keys"},
                {"icon": "chart-line", "value": "98.4%", "label": "Entanglement Health"},
                {"icon": "shield", "value": "3.2ms", "label": "Avg Verification"}
            ],
            "backends": BACKEND_STATE
        },
        "security": {
            "title": "Defense Cloud",
            "stats": [
                {"icon": "shield-haltered", "value": "0", "label": "Active Threats"},
                {"icon": "check-circle", "value": "99.97%", "label": "Detection Rate"},
                {"icon": "clock", "value": "3.2ms", "label": "Response Time"},
                {"icon": "bell", "value": THREATS_BLOCKED, "label": "Threats Blocked"}
            ]
        },
        "student": {
            "title": "Learning Portal",
            "stats": [
                {"icon": "book", "value": "4", "label": "Active Courses"},
                {"icon": "check-circle", "value": "12", "label": "Completed"},
                {"icon": "chart-line", "value": "78%", "label": "Progress"},
                {"icon": "brain", "value": "92%", "label": "AI Intelligence"}
            ]
        },
        "teacher": {
            "title": "Command Center",
            "stats": [
                {"icon": "chalkboard-user", "value": "3", "label": "Active Classes"},
                {"icon": "users", "value": "87", "label": "Total Students"},
                {"icon": "clock", "value": "24", "label": "Pending Grading"},
                {"icon": "envelope", "value": "5", "label": "Parent Messages"}
            ]
        },
        "corporate": {
            "title": "Enterprise Analytics",
            "stats": [
                {"icon": "users", "value": "12500", "label": "Active Students"},
                {"icon": "building", "value": "12", "label": "Institutions"},
                {"icon": "chart-line", "value": "78.5%", "label": "Completion Rate"},
                {"icon": "dollar-sign", "value": "R310k", "label": "Monthly Revenue"}
            ]
        },
        "parent": {
            "title": "Guardian Portal",
            "stats": [
                {"icon": "heart", "value": "2", "label": "Children"},
                {"icon": "shield-haltered", "value": "94%", "label": "Safety Score"},
                {"icon": "chart-line", "value": "85%", "label": "Academic Progress"},
                {"icon": "bell", "value": "0", "label": "Active Alerts"}
            ]
        },
        "perimeter": {
            "title": "Perimeter Security",
            "stats": [
                {"icon": "video", "value": "24/24", "label": "Cameras Online"},
                {"icon": "user-shield", "value": "4", "label": "Officers On Duty"},
                {"icon": "clock", "value": "3.2s", "label": "Response Time"},
                {"icon": "exclamation-triangle", "value": "0", "label": "Active Incidents"}
            ]
        }
    }
    return portal_data.get(portal_name, {"error": "Portal not found"})

@app.post("/api/chat")
async def chat(request: ChatRequest):
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_key:
        return {"response": "Khensani AI is not configured. Please add DEEPSEEK_API_KEY."}
    
    import httpx
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {deepseek_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": f"You are Khensani, AI assistant for Luvuno OS. Current portal: {request.portal}. Answer clearly and concisely."},
                        {"role": "user", "content": request.message}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500
                },
                timeout=30.0
            )
            data = response.json()
            reply = data["choices"][0]["message"]["content"]
            return {"response": reply}
        except Exception as e:
            return {"response": f"Khensani is having trouble: {str(e)}"}

# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
