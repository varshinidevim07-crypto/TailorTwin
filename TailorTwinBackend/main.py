import firebase_admin
from firebase_admin import credentials, firestore
from fastapi.responses import StreamingResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from routes.measurements import router as measurements_router
from routes.patterns import router as patterns_router
from routes.fabric import router as fabric_router
from routes.pdf import router as pdf_router
from routes.pdf import router as pdf_router
app = FastAPI(
    title="TailorTwin Backend",
    description="Backend for TailorTwin Custom Clothing Application",
    version="1.0.0"
)
app.include_router(measurements_router)
app.include_router(patterns_router)
app.include_router(fabric_router)
app.include_router(pdf_router)
app.include_router(pdf_router)
# Firebase Connection

from firebase_config import db

@app.get("/")
def home():
    return {
        "project": "TailorTwin",
        "message": "Backend is running successfully!",
        "status": "Success"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "TailorTwin API"
    }
# Customer Measurement Model

class Measurement(BaseModel):

    height: float = Field(gt=0)
    bust: float = Field(gt=0)
    waist: float = Field(gt=0)
    hip: float = Field(gt=0)
    shoulder: float = Field(gt=0)
    sleeve: float = Field(gt=0)


# ==========================================
# GARMENT PATTERN GENERATION API
# ==========================================



class PatternRequest(BaseModel):

    garment: str

    # Main body measurements
    height: float = Field(gt=0)
    bust: float = Field(gt=0)
    waist: float = Field(gt=0)
    hip: float = Field(gt=0)

    # Shoulder and sleeve measurements
    shoulder: float = Field(gt=0)
    sleeve: float = Field(gt=0)
    armhole: float = Field(gt=0)
    neck: float = Field(gt=0)
    upper_arm: float = Field(gt=0)


# ==========================================
# FABRIC REQUIREMENT CALCULATION API
# ==========================================

class FabricRequest(BaseModel):

    garment: str

    height: float = Field(gt=0)
    bust: float = Field(gt=0)
    waist: float = Field(gt=0)
    hip: float = Field(gt=0)

    fabric_width: float = Field(default=150, gt=0)

@app.get("/firebase-test")
def firebase_test():

    db.collection("connection_test").document("test").set({
        "message": "TailorTwin Firebase Connected!",
        "status": "success"
    })

    return {
        "message": "Firebase connected successfully!",
        "status": "success"
    }


