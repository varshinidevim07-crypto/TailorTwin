
from fastapi import APIRouter, HTTPException

from models import Measurement
from firebase_config import db

router = APIRouter()


@router.post("/measurements")
def calculate_measurements(data: Measurement):

    try:
        measurement_data = {
            "height": data.height,
            "bust": data.bust,
            "waist": data.waist,
            "hip": data.hip,
            "shoulder": data.shoulder,
            "sleeve": data.sleeve
        }

        doc_ref = db.collection("customers").add({
            "measurements_cm": measurement_data,
            "status": "success"
        })

        return {
            "message": "Measurements saved successfully!",
            "customer_id": doc_ref[1].id,
            "measurements_cm": measurement_data,
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save measurements: {str(e)}"
        )
