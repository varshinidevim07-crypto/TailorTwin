
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
from reportlab.pdfgen import canvas

from models import PatternRequest

router = APIRouter()

@router.post("/patterns/pdf")
def generate_pattern_pdf(data: PatternRequest):

    garment = data.garment.lower()

    if garment not in ["blouse", "kurta", "salwar"]:
        raise HTTPException(
            status_code=400,
            detail="Choose blouse, kurta or salwar"
        )

    # Seam and ease allowances
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

    # Calculate pattern dimensions
    bust_width = round((data.bust + ease) / 4, 2)
    waist_width = round((data.waist + ease) / 4, 2)
    hip_width = round((data.hip + ease) / 4, 2)
    garment_length = round(length, 2)

    pattern_width = max(
        bust_width,
        waist_width,
        hip_width
    )

    # Create PDF in memory
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=(595, 842))

    # PDF heading
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, 790, "TailorTwin - Garment Pattern")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 755, f"Garment: {garment.upper()}")

    pdf.drawString(50, 730, "Customer Measurements (cm)")

    pdf.drawString(50, 705, f"Height: {data.height}")
    pdf.drawString(50, 685, f"Bust: {data.bust}")
    pdf.drawString(50, 665, f"Waist: {data.waist}")
    pdf.drawString(50, 645, f"Hip: {data.hip}")

    pdf.drawString(50, 610, "Pattern Dimensions (cm)")

    pdf.drawString(50, 585, f"Bust Width: {bust_width}")
    pdf.drawString(50, 565, f"Waist Width: {waist_width}")
    pdf.drawString(50, 545, f"Hip Width: {hip_width}")
    pdf.drawString(50, 525, f"Garment Length: {garment_length}")

    pdf.drawString(
        50, 500,
        f"Seam Allowance: {seam_allowance} cm"
    )

    # Draw a basic schematic pattern
    # Scale drawing to fit the A4 page
    scale = min(
        300 / (pattern_width + 2 * seam_allowance),
        430 / (garment_length + 2 * seam_allowance)
    )

    drawing_width = (
        pattern_width + 2 * seam_allowance
    ) * scale

    drawing_height = (
        garment_length + 2 * seam_allowance
    ) * scale

    x = (595 - drawing_width) / 2
    y = 60

    # Outer cutting boundary
    pdf.setLineWidth(2)
    pdf.rect(
        x,
        y,
        drawing_width,
        drawing_height
    )

    # Inner stitching boundary
    pdf.setDash(4, 3)
    pdf.rect(
        x + seam_allowance * scale,
        y + seam_allowance * scale,
        pattern_width * scale,
        garment_length * scale
    )

    pdf.setDash()

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(
        x,
        y + drawing_height + 12,
        "Outer line: Cutting boundary"
    )

    pdf.drawString(
        x,
        y - 15,
        "Dashed line: Stitching boundary"
    )

    pdf.drawString(
        50,
        25,
        "Basic schematic pattern - verify fit and drafting before cutting fabric."
    )

    pdf.save()

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            f"attachment; filename=TailorTwin_{garment}_pattern.pdf"
        }
    )

@router.post("/patterns/kurta-pdf")
def generate_kurta_pdf(data: PatternRequest):
    print("KURTA PDF ROUTE IS EXECUTING!")

    garment = data.garment.lower()

    if garment != "kurta":
        raise HTTPException(
            status_code=400,
            detail="This endpoint currently generates kurta patterns only"
        )

    # Basic tailoring allowances
    seam = 1.5
    ease = 6

    # Calculate garment dimensions
    bust_width = (data.bust + ease) / 4
    waist_width = (data.waist + ease) / 4
    hip_width = (data.hip + ease) / 4

    width = max(bust_width, waist_width, hip_width)
    length = data.height * 0.75

    # Estimate armhole depth from available measurements.
    # data.armhole is treated as armhole circumference.
    armhole_depth = max(
        16,
        min(data.armhole * 0.5 + 2, data.bust / 6 + 8)
    )

    armhole_depth = min(armhole_depth, length * 0.35)

    # Estimate neckline dimensions
    neck_width = min(data.neck / 6, width * 0.40)

    front_neck_depth = min(data.neck / 5, 10)
    back_neck_depth = min(data.neck / 15, 3)

    # Shoulder dimensions
    shoulder_x = min(data.shoulder / 2, width * 0.85)
    shoulder_drop = 2.5

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=(595, 842))

    # Draw body pattern
    def draw_body(title, neck_depth):

        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(40, 800, "TailorTwin - Kurta Pattern")

        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(40, 775, title)

        pdf.setFont("Helvetica", 9)

        pdf.drawString(40, 755, f"Bust: {data.bust} cm")
        pdf.drawString(40, 740, f"Waist: {data.waist} cm")
        pdf.drawString(40, 725, f"Hip: {data.hip} cm")
        pdf.drawString(40, 710, f"Shoulder: {data.shoulder} cm")
        pdf.drawString(40, 695, f"Neck width: {neck_width:.2f} cm")
        pdf.drawString(40, 680, f"Armhole depth (estimated): {armhole_depth:.2f} cm")
        pdf.drawString(40, 665, f"Body width: {width:.2f} cm")
        pdf.drawString(40, 650, f"Garment length: {length:.2f} cm")
        pdf.drawString(40, 635, f"Seam allowance: {seam} cm")

        # Fit pattern on PDF page
        cut_width = width + 2 * seam
        cut_height = length + 2 * seam

        scale = min(
            310 / cut_width,
            510 / cut_height
        )

        x = (595 - cut_width * scale) / 2
        y = 90

        pdf.saveState()
        pdf.translate(x, y)
        pdf.scale(scale, scale)

        # Draw cutting boundary
        cut = pdf.beginPath()

        cut.moveTo(0, 0)
        cut.lineTo(cut_width, 0)

        cut.lineTo(
            cut_width,
            cut_height - armhole_depth - seam
        )

        cut.curveTo(
            cut_width * 0.98,
            cut_height - armhole_depth * 0.4,
            shoulder_x + seam + 4,
            cut_height - shoulder_drop,
            shoulder_x + seam,
            cut_height - shoulder_drop
        )

        cut.lineTo(neck_width + seam, cut_height)

        cut.curveTo(
            neck_width * 0.6 + seam,
            cut_height,
            seam,
            cut_height - neck_depth * 0.35,
            seam,
            cut_height - neck_depth - seam
        )

        cut.lineTo(0, 0)
        cut.close()

        pdf.setLineWidth(1.5 / scale)
        pdf.setDash()
        pdf.drawPath(cut, stroke=1, fill=0)

        # Draw stitching boundary
        pdf.saveState()
        pdf.translate(seam, seam)

        stitch = pdf.beginPath()

        stitch.moveTo(0, 0)
        stitch.lineTo(width, 0)

        stitch.lineTo(
            width,
            length - armhole_depth
        )

        stitch.curveTo(
            width * 0.98,
            length - armhole_depth * 0.4,
            shoulder_x + 4,
            length - shoulder_drop,
            shoulder_x,
            length - shoulder_drop
        )

        stitch.lineTo(neck_width, length)

        stitch.curveTo(
            neck_width * 0.6,
            length,
            0,
            length - neck_depth * 0.35,
            0,
            length - neck_depth
        )

        stitch.lineTo(0, 0)
        stitch.close()

        pdf.setLineWidth(1 / scale)
        pdf.setDash(3 / scale, 2 / scale)
        pdf.drawPath(stitch, stroke=1, fill=0)

        pdf.restoreState()

        # Centre fold line
        pdf.setDash(4 / scale, 3 / scale)
        pdf.line(
            seam,
            seam,
            seam,
            length + seam
        )

        # Grainline
        pdf.setDash()
        pdf.setLineWidth(1 / scale)

        grain_x = seam + width * 0.12

        pdf.line(
            grain_x,
            seam + 15,
            grain_x,
            length + seam - 15
        )

        pdf.restoreState()

        # Instructions
        pdf.setFont("Helvetica", 8)

        pdf.drawString(40, 65, "Solid line: Cutting boundary")
        pdf.drawString(40, 52, "Dashed line: Stitching boundary")
        pdf.drawString(40, 39, "Centre line: Fold line")
        pdf.drawString(40, 26, "Draft pattern - verify measurements and fit before cutting.")

    # PAGE 1: FRONT
    draw_body("KURTA FRONT", front_neck_depth)
    pdf.showPage()

    # PAGE 2: BACK
    draw_body("KURTA BACK", back_neck_depth)
    pdf.showPage()

    # PAGE 3: SLEEVE
    def draw_sleeve():

        sleeve_length = data.sleeve

        # Estimated sleeve dimensions
        sleeve_width = data.upper_arm + 8

        sleeve_opening = max(
            data.upper_arm * 0.65,
            22
        )

        cap_height = armhole_depth * 0.65

        cut_width = sleeve_width + 2 * seam
        cut_height = sleeve_length + 2 * seam

        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(40, 800, "TailorTwin - Kurta Pattern")

        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(40, 775, "KURTA SLEEVE")

        pdf.setFont("Helvetica", 9)
        pdf.drawString(40, 755, f"Sleeve length: {sleeve_length} cm")
        pdf.drawString(40, 740, f"Upper arm: {data.upper_arm} cm")
        pdf.drawString(40, 725, f"Sleeve width: {sleeve_width} cm")
        pdf.drawString(40, 710, f"Sleeve opening (estimated): {sleeve_opening:.2f} cm")
        pdf.drawString(40, 695, f"Sleeve cap height (estimated): {cap_height:.2f} cm")
        pdf.drawString(40, 680, f"Seam allowance: {seam} cm")

        scale = min(
            420 / cut_width,
            500 / cut_height
        )

        x = (595 - cut_width * scale) / 2
        y = 100

        pdf.saveState()
        pdf.translate(x, y)
        pdf.scale(scale, scale)

        # Cutting boundary
        outer = pdf.beginPath()

        outer.moveTo(seam, seam + sleeve_length - cap_height)

        outer.curveTo(
            seam,
            seam + sleeve_length - cap_height * 0.2,
            seam + sleeve_width * 0.2,
            seam + sleeve_length + seam,
            seam + sleeve_width / 2,
            seam + sleeve_length + seam
        )

        outer.curveTo(
            seam + sleeve_width * 0.8,
            seam + sleeve_length + seam,
            seam + sleeve_width + seam,
            seam + sleeve_length - cap_height * 0.2,
            seam + sleeve_width + seam,
            seam + sleeve_length - cap_height
        )

        outer.lineTo(
            seam + (sleeve_width + sleeve_opening) / 2,
            seam
        )

        outer.lineTo(
            seam + (sleeve_width - sleeve_opening) / 2,
            seam
        )

        outer.close()

        pdf.setLineWidth(1.5 / scale)
        pdf.drawPath(outer, stroke=1, fill=0)

        # Stitching boundary
        pdf.saveState()
        pdf.translate(seam, seam)

        inner = pdf.beginPath()

        inner.moveTo(0, sleeve_length - cap_height)

        inner.curveTo(
            0,
            sleeve_length - cap_height * 0.2,
            sleeve_width * 0.2,
            sleeve_length,
            sleeve_width / 2,
            sleeve_length
        )

        inner.curveTo(
            sleeve_width * 0.8,
            sleeve_length,
            sleeve_width,
            sleeve_length - cap_height * 0.2,
            sleeve_width,
            sleeve_length - cap_height
        )

        inner.lineTo(
            (sleeve_width + sleeve_opening) / 2,
            0
        )

        inner.lineTo(
            (sleeve_width - sleeve_opening) / 2,
            0
        )

        inner.close()

        pdf.setDash(3 / scale, 2 / scale)
        pdf.drawPath(inner, stroke=1, fill=0)

        pdf.restoreState()

        # Sleeve grainline
        pdf.setDash(4 / scale, 3 / scale)

        pdf.line(
            cut_width / 2,
            seam + 5,
            cut_width / 2,
            cut_height - 5
        )

        pdf.restoreState()

        pdf.setFont("Helvetica", 8)
        pdf.drawString(40, 65, "Solid line: Cutting boundary")
        pdf.drawString(40, 52, "Dashed line: Stitching boundary")
        pdf.drawString(40, 39, "Centre line: Grainline")
        pdf.drawString(40, 26, "Sleeve opening is estimated; verify wrist fit.")
    print("Generating sleeve page...")
    draw_sleeve()
    print("Sleeve page generated successfully!")

    pdf.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=TailorTwin_Kurta_Three_Piece.pdf"
        }
    )