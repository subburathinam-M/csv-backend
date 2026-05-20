from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.services.csv_service import process_csv  # ← app. add pannanum


router = APIRouter(prefix="/api/v1/csv", tags=["CSV Processor"])


@router.post("/process")
async def process_csv_file(file: UploadFile = File(...)):
    """
    Upload a CSV file → Download ZIP with 3 Excel files:
    - duplicates.xlsx        → all duplicate rows
    - unique.xlsx            → unique rows only
    - duplicate_grouped.xlsx → duplicate values in single column
    """

    # ── Validate file type ───────────────────────────────
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only .csv files are allowed"
        )

    # ── Read file bytes ──────────────────────────────────
    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    # ── Process CSV ──────────────────────────────────────
    try:
        zip_buffer, stats = process_csv(file_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )

    # ── Return ZIP as download ───────────────────────────
    headers = {
        "Content-Disposition": "inline; filename=processed_output.zip",
        "X-Total-Rows":        str(stats["total_rows"]),
        "X-Duplicate-Rows":    str(stats["duplicate_rows"]),
        "X-Unique-Rows":       str(stats["unique_rows"]),
    }

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers=headers,
    )