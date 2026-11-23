
from fastapi import APIRouter

from models import FabricRequest

router = APIRouter()


@router.post("/fabric/calculate")
def calculate_fabric(data: FabricRequest):

    garment = data.garment.lower()

    if garment not in ["blouse", "kurta", "salwar"]:
        return {
            "status": "error",
            "message": "Choose blouse, kurta or salwar"
        }

    if garment == "blouse":
        fabric_required = 1.0

    elif garment == "kurta":
        fabric_required = 2.5

    else:
        fabric_required = 2.5

    if data.bust > 110 or data.hip > 110:
        fabric_required += 0.25

    if data.fabric_width < 115:
        fabric_required *= 1.35

    fabric_required += 0.20

    return {
        "status": "success",
        "message": "Fabric requirement calculated successfully",
        "garment": garment,
        "fabric_width_cm": data.fabric_width,
        "fabric_required_metres": round(fabric_required, 2)
    }
