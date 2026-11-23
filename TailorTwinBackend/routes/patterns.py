
from fastapi import APIRouter

from models import PatternRequest

router = APIRouter()


@router.post("/patterns/generate")
def generate_pattern(data: PatternRequest):

    garment = data.garment.lower()

    if garment not in ["blouse", "kurta", "salwar"]:
        return {
            "status": "error",
            "message": "Choose blouse, kurta or salwar"
        }

    seam_allowance = 1.5

    if garment == "blouse":
        ease = 2
        length = data.height * 0.25

    elif garment == "kurta":
        ease = 6
        length = data.height * 0.75

    else:
        ease = 4
        length = data.height * 0.40

    pattern = {
        "bust_width": round((data.bust + ease) / 4, 2),
        "waist_width": round((data.waist + ease) / 4, 2),
        "hip_width": round((data.hip + ease) / 4, 2),
        "garment_length": round(length, 2),
        "seam_allowance": seam_allowance
    }

    return {
        "status": "success",
        "message": "Pattern dimensions generated successfully",
        "garment": garment,
        "measurements_cm": {
            "bust": data.bust,
            "waist": data.waist,
            "hip": data.hip,
            "height": data.height
        },
        "pattern_dimensions_cm": pattern
    }
